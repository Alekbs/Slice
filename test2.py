from proglog import ProgressBarLogger
from moviepy.editor import VideoFileClip
from time import sleep
import flet as ft
import asyncio

class MyBarLogger(ProgressBarLogger):
    
    async def callback(self, **changes):
        # Every time the logger message is updated, this function is called with
        # the `changes` dictionary of the form `parameter: new value`.
        for (parameter, value) in changes.items():
            print ('Parameter %s is now %s' % (parameter, value))
    
    async def bars_callback(self, bar, attr, value,old_value=None):
        # Every time the logger progress is updated, this function is called        
        percentage = (value / self.bars[bar]['total']) * 100
        print("% = ", percentage)
        self.percentage = percentage
    

async def main(page: ft.Page):
    global pb 
    pb= ft.ProgressBar(width=400)
    logger=MyBarLogger()
    async def convert(mp3_file,mp4_file):
        print("Началась конвертация")

        videoclip = VideoFileClip(mp4_file)
        audioclip = videoclip.audio
        audioclip.write_audiofile(mp3_file, logger=logger)
        pb.value = logger.percentage
        print(f"pb = {pb.value}")
        audioclip.close()
        videoclip.close()
        print("Закончилась конвертация")pip install trio


    
    print("Добавлены элементы")
    await page.add_async(
        ft.Text("Linear progress indicator", style="headlineSmall"),
        ft.Column([ ft.Text("Doing something..."), pb]),
    )
    async def start_convert(audio, test):
        print("Запуск конвертации")
        page.update_async()
        print("Страница обновилась_1")
        sleep(0.1)
        asyncio.create_task(convert(audio, test))
        page.update_async()
        print("Страница обновилась")
        sleep(0.1)
    
    await start_convert("audio.mp3", "test.mp4")

ft.app(target=main)
