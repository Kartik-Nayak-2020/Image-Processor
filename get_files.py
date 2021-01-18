import os
from tkinter import Tk, filedialog
import fillchar

image_extensions = ('.png', '.jpg', 'jfif', 'jpeg')
selected_images = []
image_folder_path = []


def select_files_menu():
    while True:
        if not len(selected_images) == 0:
            if len(selected_images) > 3:
                ch = "....."
            else:
                ch = ""
            while True:
                print(
                    f"Selected DIR: {image_folder_path}\nSelected Images: [{len(selected_images)}] => "
                    f"{[x for x in selected_images][:3]}{ch}\n{fillchar.draw_line()}")
                user_choice = input(
                    f"1. Change DIR/Image selection\n2. Continue with the selection\n{fillchar.draw_line()}\nUSER:")
                if user_choice == '1':
                    selected_images.clear()
                    image_folder_path.clear()
                    select_dir_files()
                elif user_choice == '2':
                    return image_folder_path, selected_images
                else:
                    print("Enter a valid option")
                    continue
                break
        else:
            select_dir_files()


def select_dir_files():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    fillchar.main_menu(" Image Processor v1.1.0 ")
    while True:
        user_choice = input(
            f"1. Select directory\n2. Select image\n3. Exit\n{fillchar.draw_line()}\nUSER:")
        if user_choice == '1':
            image_folder = filedialog.askdirectory()
            if image_folder:
                for item in os.listdir(image_folder):
                    if item.endswith(image_extensions):
                        selected_images.append(item)
            else:
                fillchar.in_between("Directory opening terminated by user")
                continue

        elif user_choice == '2':
            image_selection = list(filedialog.askopenfilenames(
                filetypes=[("All Files", ".*")]))
            if image_selection:
                image_selection_path = image_selection[0]
                image_folder = '/'.join(image_selection_path.split('/')[:-1:])
                for image in image_selection:
                    image = image.split('/')[-1::]
                    selected_images.extend(
                        [x for x in image if str(x).endswith(image_extensions)])
            else:
                fillchar.in_between("No files were selected")
                continue

        elif user_choice == '3':
            print("Application terminated by USER")
            exit()

        else:
            fillchar.in_between("Enter a valid choice!")

        if len(selected_images) != 0:
            image_folder_path.append(image_folder)
            break
        break

    if len(selected_images) == 0:
        fillchar.in_between("Directory doesn't contain any images")
        select_dir_files()


if __name__ == "__main__":
    select_files_menu()
