# src/data_interface.py

# 控制是否使用模拟数据

# 实现 load_a111_data() 读取真实 A111 数据
# 把 data_interface.py 里 USE_MOCK = False


USE_MOCK = True

if USE_MOCK:
    from .data_loader import load_mock_breathing_data as get_breathing_data
else:
    from .a111_interface import load_a111_data as get_breathing_data
