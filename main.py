from get_files import select_files_menu
from get_edits import select_edits
from apply_edits import apply_edits_main


def main():
    '''Main function of the program that executes every function in the program'''
    image_folder, selected_images = select_files_menu()
    finalized_edit_selection = select_edits()
    apply_edits_main(image_folder, selected_images, finalized_edit_selection)


if __name__ == "__main__":
    main()
