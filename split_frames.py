import os


def split_frames(video, output_path):
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    
    cmd = 'ffmpeg -i ' + video + ' -r 1/1 ' + output_path + '/frame%03d.bmp'
    os.system(cmd)