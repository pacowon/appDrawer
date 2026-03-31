"""
서브프로세스로 실행되는 카운트 워커.
stdout으로 숫자를 출력하면 부모 프로세스가 읽어서 UI에 표시.
"""
import time
import sys

for i in range(1, 21):
    print(i, flush=True)
    time.sleep(1)
