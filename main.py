from moviepy.editor import VideoFileClip
import flet as ft
import os
from tqdm import tqdm
import sys


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    #Выделение адио из видеофайла
    def extract_audio_from_video(e):
        try:
            print("Загрузка видео")
            video_clip = VideoFileClip(selected_files.value)

            print("Извлечение аудио")
            audio_clip = video_clip.audio

            print("Определение уникального имени")
            output_audio_path = find_available_filename()

            """# Определение количества итераций для tqdm
            total_iterations = int(audio_clip.duration * audio_clip.fps)

            # Сохранение аудио в формате mp3 с прогресс-баром
            pbar = tqdm(total=total_iterations, dynamic_ncols=True, unit='frame', file=sys.stdout)
            for _ in audio_clip.iter_frames():
                pbar.update()"""

            print("Сохранение аудио в формате mp3")
            audio_clip.write_audiofile(output_audio_path, codec='mp3')
            
            audio_clip.close()
            video_clip.close()

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