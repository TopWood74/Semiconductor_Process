# Semiconductor_Process

- 반도체 검사 프로젝트 (YOLOv5)
  - python 3.7.11
  - django 3.2.12

기반으로 web 서비스 진행

## 추가해야 할 파일
- db.sqlite3
- /yolov5/yolov5_chip.pt (사용자 모델파일)


## 프로젝트 폴더에서 yolov5를 다운받아 설치
git clone https://github.com/ultralytics/yolov5 (git 소스로 작업시 설치되어 있임)
cd yolov5/
pip install -qr requirements.txt


## 설치된 yolov5 폴더에 있는 detect.py 를 detect_django.py 로 복사 (소스에 있는 detect_django.py 를 복사해서 사용가능)
detect.py 를 django 에 맞게 변형 (git 소스 detect_django.py 참고 => 복사해서 사용하는 편함)

- 수정된 내용 일부
```
def run() => def run_yolo_image()
img_tensor = []

	# Write results
	for *xyxy, conf, cls in reversed(det):

            if len(det):
                list_tenser = [p.name, det.numpy()]
            else:
                list_tenser = [p.name, None]
            img_tensor.append(list_tenser)
                        
            # Stream results
            im0 = annotator.result()

    ~~~

    # print("save_dir", str(save_dir))
    rvalue = {'save_dir': str(save_dir), 'img_tensor': img_tensor}

    del model
    del img_tensor
    gc.collect()

    return rvalue
```

## detect_django.py 에서 메모리 반납이 잘 되지 않아서 추가
```
import gc

    del model
    del img_tensor
    gc.collect()
```
를 사용하여 반납


## 서비스 할 app 에  views.py 파일 상단에 import
- import yolov5.detect_django as yolo
=> 오류시 /program/ 폴더로 yolov5를 복사!!!

- views.py 내용중 환경에 맞게 경로 수정
```
base_url2 = save_dir.replace("/mnt/c/Users/admin/workspace/web_project/_media/screening_ab2", base_url2)
```

## 다운받은 yolov5 은  yolov5 폴더에서 실행해야 오류가 없음
- django 의 app 에서 실행되기 때문에 실행해 가면서 yolov5 의  import 된 모듈의 경로를 수정
- from utils import TryExcept => from yolov5.utils import TryExcept
