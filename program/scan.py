# Library Import
import sys
import numpy as np
import cv2
import os
from django.conf import settings

def crop(path, img):
    #filename_path = "/mnt/c/Users/admin/workspace/cakd7_dj/"
    filename_path = str(settings.BASE_DIR) + "/"

    img_path = filename_path + path + "/" + img
    print(img_path)

    # crop image
    img_name, img_ext = os.path.splitext(img)
    img_name += "_crop"

    # 입력 이미지 불러오기
    src = cv2.imread(img_path)
    if src is None:
        print("Image open failed!")
        #src = cv2.imread("/mnt/c/Users/admin/workspace/cakd7_dj/_media/scanned.jpg")

    if src is None:
        return ''

    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _, src_bin = cv2.threshold(src_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(src_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # 입력 영상 크기 및 출력 영상 크기
    h, w = src.shape[:2]
    dw = 500
    dh = round(dw * 297 / 210)  # A4 용지 크기: 210x297cm

    # 모서리 점들의 좌표, 드래그 상태 여부
    srcQuad = np.array([[30, 30], [30, h - 30], [w - 30, h - 30], [w - 30, 30]], np.float32) # 내가 선택할 모서리 좌표들 ndarray 반시계방향
    dstQuad = np.array([[0, 0], [0, dh - 1], [dw - 1, dh - 1], [dw - 1, 0]], np.float32)
    dragSrc = [False, False, False, False] # 현재 어떤 점을 드래그 하고 있나의 Flag

    cont = [c for c in contours if cv2.contourArea(c) > 1000]

    for pts in cont:
        # 외곽선 근사화
        approx = cv2.approxPolyDP(pts, cv2.arcLength(pts, True) * 0.02, True)
        # 컨벡스가 아니고, 사각형이 아니면 무시
        if not cv2.isContourConvex(approx) or len(approx) != 4:
            continue
        srcQuad = reorderPts(approx.reshape(4, 2).astype(np.float32))

    # 모서리점, 사각형 그리기
    disp = drawROI(src, srcQuad)
    #cv2.imshow("img", disp)
    #cv2.setMouseCallback("img", onMouse)

    # 투시 변환
    # 왜곡된 문서 영상을 직사각형 형태로 똑바로 펴기
    pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
    dst = cv2.warpPerspective(src, pers, (dw, dh), flags=cv2.INTER_CUBIC)

    # 직사각형 이미지 저장
    cv2.imwrite(filename_path+path+"/"+img_name+img_ext, dst)

    return img_name+img_ext

def drawROI(img, corners):
    """네 꼭지점 사이에 선을 그린다."""
    cpy = img.copy()

    c1 = (192, 192, 255) # 조금 연한 핑크. 원 그리기에 사용
    c2 = (128, 128, 255) # 조금 탁한 핑크. 선 그리기에 사용

    # 4개의 모서리에 c1 색으로 원을 그린다.
    for pt in corners:
        cv2.circle(cpy, tuple(pt.astype(int)), 25, c1, -1, cv2.LINE_AA)
    
    # 4개의 모서리 각각의 사이에 선을 그린다. 
    cv2.line(cpy, tuple(corners[0].astype(int)), tuple(corners[1].astype(int)), c2, 2, cv2.LINE_AA)
    cv2.line(cpy, tuple(corners[1].astype(int)), tuple(corners[2].astype(int)), c2, 2, cv2.LINE_AA)
    cv2.line(cpy, tuple(corners[2].astype(int)), tuple(corners[3].astype(int)), c2, 2, cv2.LINE_AA)
    cv2.line(cpy, tuple(corners[3].astype(int)), tuple(corners[0].astype(int)), c2, 2, cv2.LINE_AA)
    
    # 이 함수 안에서 그린 이미지와 원래 이미지를 7:3 비율로 겹쳐서 반환한다.
    disp = cv2.addWeighted(img, 0.3, cpy, 0.7, 0)

    return disp

def reorderPts(pts):
    """왼쪽 위 모서리부터 시작해서 반시계 방향으로 0,1,2,3번째 포인트가 되도록 순서를 조정한다."""
    idx = np.lexsort((pts[:, 1], pts[:, 0]))  # 칼럼0 -> 칼럼1 순으로 정렬한 인덱스를 반환
    pts = pts[idx]  # x좌표로 정렬

    if pts[0, 1] > pts[1, 1]:
        pts[[0, 1]] = pts[[1, 0]]

    if pts[2, 1] < pts[3, 1]:
        pts[[2, 3]] = pts[[3, 2]]

    return pts