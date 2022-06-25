# https://hub.docker.com/r/paddlepaddle/paddle/tags/
ARG PADDLE="1.10.0"
ARG CUDA="11.2"
ARG CUDNN="8"

FROM paddlepaddle/paddle:${PADDLE}-gpu-cuda${CUDA}-cudnn${CUDNN}

RUN pip install \
    paddleocr>=2.0.1 \
    gpxpy==1.5.0 \
    pydantic==1.9.1 \
    loguru==0.6.0 \
    opencv-contrib-python

RUN pip3 install -U \
    https://paddleocr.bj.bcebos.com/whl/layoutparser-0.0.0-py3-none-any.whl

# RUN curl --create-dir https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_det_infer.tar \
#     -o /root/.paddleocr/whl/det/en/en_PP-OCRv3_det_infer/en_PP-OCRv3_det_infer.tar && \
#     tar -xvf /root/.paddleocr/whl/det/en/en_PP-OCRv3_det_infer/en_PP-OCRv3_det_infer.tar -C /root/.paddleocr/whl/det/en/ && \
#     rm /root/.paddleocr/whl/det/en/en_PP-OCRv3_det_infer/en_PP-OCRv3_det_infer.tar
    
# RUN curl --create-dir https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_rec_infer.tar \
#     -o /root/.paddleocr/whl/rec/en/en_PP-OCRv3_rec_infer/en_PP-OCRv3_rec_infer.tar && \
#     tar -xvf /root/.paddleocr/whl/rec/en/en_PP-OCRv3_rec_infer/en_PP-OCRv3_rec_infer.tar -C /root/.paddleocr/whl/rec/en/ && \
#     rm /root/.paddleocr/whl/rec/en/en_PP-OCRv3_rec_infer/en_PP-OCRv3_rec_infer.tar

# RUN curl --create-dir https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar \
#     -o /root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer/ch_ppocr_mobile_v2.0_cls_infer.tar && \
#     tar -xvf /root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer/ch_ppocr_mobile_v2.0_cls_infer.tar -C /root/.paddleocr/whl/cls && \
#     rm /root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer/ch_ppocr_mobile_v2.0_cls_infer.tar

COPY ./whl/ /root/.paddleocr/whl/

WORKDIR /gps_ocr

COPY ./fonts/ ./fonts/
COPY ./main.py .

ENTRYPOINT ["python3", "/gps_ocr/main.py"]
CMD ["--help"]