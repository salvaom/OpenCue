@echo off

for /F "tokens=*" %%A in ('dir /B *.proto') do (
    python -m grpc_tools.protoc -I=. --python_out=../pycue/opencue/compiled_proto --grpc_python_out=../pycue/opencue/compiled_proto ./%%A
)
