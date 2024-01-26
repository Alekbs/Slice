from moviepy.editor import VideoFileClip
import flet as ft
import os
from proglog import ProgressBarLogger

class MyBarLogger(ProgressBarLogger):

    def __init__(self, ft_pb: ft.ProgressBar):
        super().__init__()
        self._ft_pb = ft_pb

    def bars_callback(self, bar, attr, value, old_value=None):
        percentage = (value / self.bars[bar]['total'])
        #print("% = ", percentage)
        self._ft_pb.value = percentage
        self._ft_pb.update()

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    pb = ft.ProgressBar(width=400, visible=False)
    logger = MyBarLogger(pb)
    Succes_text = ft.Text("Конвертация успешна", visible=False)
    #Выделение адио из видеофайла
    def extract_audio_from_video(e):
        try:
            Succes_text = ft.Text(visible=False)
            print("Загрузка видео")
            video_clip = VideoFileClip(selected_files.value)

            print("Извлечение аудио")
            audio_clip = video_clip.audio

            print("Определение уникального имени")
            output_audio_path = find_available_filename()

            pb.visible = True
            print("Сохранение аудио в формате mp3")
            audio_clip.write_audiofile(output_audio_path, codec='mp3', logger=logger)
            
            audio_clip.close()
            video_clip.close()
            pb.visible = False
            Succes_text.visible = True
            page.update()
            
            print("Аудио успешно извлечено и сохранено в", output_audio_path)

        except Exception as e:
            print("Произошла ошибка:", str(e))

    #Выбор видео
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "Cancelled!"
        )

        selected_files.update()
    
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()
    

    # hide all dialogs in overlay
    page.overlay.extend([pick_files_dialog]) 

    #Сохранение аудио
    def find_available_filename():
        counter = 1
        while True:
            new_filename = f"temp_audio_{counter}.mp3"
            full_path = os.path.join("temp", new_filename)
            if not os.path.exists(full_path):
                return full_path
            counter += 1




    page.add(
        ft.Row(
            [
                #txt_number,
                ft.ElevatedButton(
                    "Pick files",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True
                    ),
                ),
                selected_files,
                ft.IconButton(ft.icons.PLAY_ARROW, on_click=extract_audio_from_video),
                Succes_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            
        ),
        ft.Row(
            [
                pb,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )   
    # Пример использования
    """
    input_video_path = "test.mp4"
    output_audio_path = "извлеченное_аудио.mp3"
    extract_audio_from_video(input_video_path, output_audio_path)
    """
ft.app(target=main)