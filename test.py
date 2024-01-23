from proglog import ProgressBarLogger
from moviepy.editor import VideoFileClip
import flet as ft
import trio
import trio
print("trio version:", trio.__version__)

class MyBarLogger(ProgressBarLogger):
    
    async def callback(self, **changes):
        for (parameter, value) in changes.items():
            print('Parameter %s is now %s' % (parameter, value))
    
    async def bars_callback(self, bar, attr, value, old_value=None):
        percentage = (value / self.bars[bar]['total']) * 100
        print("% = ", percentage)
        self.percentage = percentage

async def convert(mp3_file, mp4_file, logger, pb):
    print("Началась конвертация")
    videoclip = VideoFileClip(mp4_file)
    audioclip = videoclip.audio

    def write_audio_file():
        audioclip.write_audiofile(mp3_file, logger=logger)
        pb.value = logger.percentage
        audioclip.close()
        videoclip.close()
        print("Закончилась конвертация")

    with trio.open_file(mp3_file, 'wb') as f:
        await trio.to_thread.run_sync(write_audio_file)



async def main(page: ft.Page):
    async def start_convert(audio, test):
        print("Запуск конвертации")
        page.update_async()
        await trio.sleep(0.1)
        await convert(audio, test, logger, pb)
        page.update_async()
        await trio.sleep(0.1)
    pb = ft.ProgressBar(width=400)
    logger = MyBarLogger()

    print("Добавлены элементы")
    await page.add_async(
        ft.Text("Linear progress indicator", style="headlineSmall"),
        ft.Column([ft.Text("Doing something..."), pb]),
    )

    # Ensure that we are running the start_convert function from an asynchronous context
    async with trio.open_nursery() as nursery:
        nursery.start_soon(start_convert, "audio.mp3", "test.mp4")

ft.app(target=main)

