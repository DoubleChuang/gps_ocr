# GPS OCR

Detect video frame that has GPS information record by [E3V device(GPS ver)](http://www.grenzel.com/ch/products6-2.html), and save it into a .gpx file

## How to use

Copy the E3V video into current directory, and then run following


```
docker run -it --rm \
    -v $PWD:/tmp1 
    -w /tmp1 \
    doublehub/gps_ocr:latest \
        -i ${YOUR_E3V_VIDEO_FILE}
```

Example:
```
docker run -it --rm \
    -v $PWD:/tmp1 
    -w /tmp1 \
    doublehub/gps_ocr:latest \
        -i ./examples/20220624223651_000060B.MP4
```

The following are to be deleted
---
## installation
https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.5/doc/doc_en/quickstart_en.md#1-installation

### python環境建置
```
# 因為官方準備環境是3.7 所以使用3.7.13的版本
ref. https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.5/doc/doc_en/environment_en.md#environment-preparation

pyenv install -v 3.7.13
pyenv virtualenv 3.7.13 gpx-ocr
pyenv activate gpx-ocr
```

### 安裝paddle package
```
# GPU
python3 -m pip install paddlepaddle-gpu
# CPU
python3 -m pip install paddlepaddle
```

### paddle OCR package

```
pip install "paddleocr>=2.0.1" # Recommend to use version 2.0.1+

pip3 install -U https://paddleocr.bj.bcebos.com/whl/layoutparser-0.0.0-py3-none-any.whl
```

### inference 目前沒以成功
```
paddleocr --image_dir ./images/1.png --det false --lang en
```


## Docker 
📦 dockerhub: https://hub.docker.com/r/paddlepaddle/paddle/tags/

```
docker run --name ppocr -v $PWD:/paddle --network=host -it   paddlepaddle/paddle:2.3.0  /bin/bash

pip install "paddleocr>=2.0.1"
pip install gpxpy==1.5.0
pip3 install -U https://paddleocr.bj.bcebos.com/whl/layoutparser-0.0.0-py3-none-any.whl
pip install pydantic
pip install loguru
wget https://github.com/Halfish/lstm-ctc-ocr/raw/master/fonts/simfang.ttf

```

build
```
docker build -t gps_ocr ./dockerfiles/cpu.dockerfile

docker run  -it --rm --name gps_ocr -v $PWD:/tmp1 -w /tmp1 gps_ocr
```

## X11 windows with Docekr on Mac

```
brew install xquartz --cask
brew install socat

# logout

open -a xquartz
```
ref:
    https://medium.com/@mreichelt/how-to-show-x11-windows-within-docker-on-mac-50759f4b65cb


Running GUI programs in Docker on macOS
    https://github.com/hybridgroup/gocv#running-gui-programs-in-docker-on-macos

## References
[opencv capture](https://medium.com/ching-i/python-opencv-%E8%AE%80%E5%8F%96%E9%A1%AF%E7%A4%BA%E5%8F%8A%E5%84%B2%E5%AD%98%E5%BD%B1%E5%83%8F-%E5%BD%B1%E7%89%87-ee3701c454da)