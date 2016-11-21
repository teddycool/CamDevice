__author__ = 'teddycool'
#TODO: Fix values according to IOTest!!!
deviceconfig = {"cam": {"res": (640, 480), "id": 1, "framerate": 20},  # CAM settings
                "Button": {"Pressed": 0.5, "LongPressed": 3},
                "IO": {"RedButton": 15, "GreenButton": 14, "GreenLed": 23, "RedLed": 24, "YellowLed": 22,
                       "Switch1.1": 21, "Switch1.2": 12},
                "Streamer": {"StreamerImage": "/tmp/stream/pic.jpg", "StreamerLib": "/tmp/stream",
                             "VideoFile": "/home/pi/CamDevice/video.mpg"},
                "Vision": {"WriteFramesToSeparateFiles": False, "PrintFrameRate": True},
                "Main": {"MaxFrameRate": 10},
               }
