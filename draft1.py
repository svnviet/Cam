import ctypes

user32 = ctypes.WinDLL('user32')

SW_MAXIMISE = 2

hWnd = user32.GetForegroundWindow()

user32.ShowWindow(hWnd, SW_MAXIMISE)
