import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from datetime import datetime
import os, platform, subprocess, sys

class MeetingNotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meeting Notes Manager")

        # Dictionary to hold all notes
        self.all_notes_dict = {}

        # Title frame for meeting
        self.title_frame = tk.Frame(self.root)
        self.title_frame.pack(pady=20)

        self.title_label = tk.Label(self.title_frame, text="Meeting Title:")
        self.title_label.pack(side=tk.LEFT)

        self.title_entry = tk.Entry(self.title_frame, width=60, insertbackground="white")
        self.title_entry.pack(side=tk.LEFT, padx=10)

        # Main frames for input and listbox
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        self.input_frame = tk.Frame(self.main_frame, bd=2, relief='ridge', padx = 10)
        self.input_frame.pack(side=tk.LEFT, padx=10)

        self.listbox_frame = tk.Frame(self.main_frame)
        self.listbox_frame.pack(side=tk.LEFT, padx=10)

        self.listbox_label = tk.Label(self.listbox_frame, text="Current Entries:")
        self.listbox_label.pack(side=tk.TOP)

        # Frame for person's name
        self.name_frame = tk.Frame(self.input_frame)
        self.name_frame.pack(pady=20)

        self.name_label = tk.Label(self.name_frame, text="Person Name:")
        self.name_label.pack(side=tk.LEFT)

        self.name_entry = tk.Entry(self.name_frame, width=50, insertbackground="white")
        self.name_entry.pack(side=tk.LEFT, padx=10)

        # Frame for notes
        self.notes_frame = tk.Frame(self.input_frame)
        self.notes_frame.pack(pady=20)

        self.notes_label = tk.Label(self.notes_frame, text="Notes:")
        self.notes_label.pack(anchor=tk.W)

        self.notes_text = scrolledtext.ScrolledText(self.notes_frame, width=80, height=10, insertbackground="white")
        self.notes_text.pack()

        # Add notes
        self.add_btn = tk.Button(self.input_frame, text="Add Notes", command=self.add_notes)
        self.add_btn.pack(pady=10)

        # Listbox for names
        self.names_listbox = tk.Listbox(self.listbox_frame, height=15, width=40)
        self.names_listbox.pack(pady=20)

        self.additional_notes_frame = tk.Frame(self.root)
        self.additional_notes_frame.pack(pady=20)

        self.additional_notes_label = tk.Label(self.additional_notes_frame, text="Additional Notes:")
        self.additional_notes_label.pack(anchor=tk.W)

        self.additional_notes_text = scrolledtext.ScrolledText(self.additional_notes_frame, width=80, height=10, insertbackground="white")
        self.additional_notes_text.pack()

        # Save button frame
        self.save_btn_frame = tk.Frame(self.root)
        self.save_btn_frame.pack(pady=20)

        self.save_btn = tk.Button(self.save_btn_frame, text="Save Notes", command=self.save_all_notes)
        self.save_btn.pack(pady=10)

        self.names_listbox.bind("<Double-1>", self.edit_note)
        self.names_listbox.bind("<Delete>", self.delete_selected_note)
        self.names_listbox.bind("<BackSpace>", self.delete_selected_note)
        self.additional_notes_text.bind("<Control-BackSpace>", self.delete_word)
        self.notes_text.bind("<Control-BackSpace>", self.delete_word)

        root.config(bg="gray25")
        self.main_frame.config(bg="gray25")
        self.name_frame.config(bg="gray25")
        self.input_frame.config(bg="gray25")
        self.notes_frame.config(bg="gray25")
        self.title_frame.config(bg="gray25")
        self.listbox_frame.config(bg="gray25")
        self.save_btn_frame.config(bg="gray25")
        self.additional_notes_frame.config(bg="gray25")
        self.names_listbox.config(bg="gray35", fg="white")
        self.name_entry.config(bg="gray35", fg="white")
        self.title_entry.config(bg="gray35", fg="white")
        self.additional_notes_text.config(bg="gray35", fg="white")
        self.notes_text.config(bg="gray35", fg="white")
        self.name_label.config(bg="gray25", fg="white")
        self.notes_label.config(bg="gray25", fg="white")
        self.title_label.config(bg="gray25", fg="white")
        self.listbox_label.config(bg="gray25", fg="white")
        self.additional_notes_label.config(bg="gray25", fg="white")
        self.add_btn.config(bg="gray55", fg="white")
        self.save_btn.config(bg="gray55", fg="white")
    
    def delete_word(self, event):
        text_widget = event.widget
        all_text = text_widget.get("1.0", "insert")
        end = len(all_text)
        start = end - 1
        while start > 0 and not all_text[start].isspace():
            start -= 1
        start_index = "1.0 + %d chars" % start
        end_index = "1.0 + %d chars" % end
        text_widget.delete(start_index, end_index)
        return "break"

    def add_notes(self):
        person_name = self.name_entry.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()

        if not person_name or not notes:
            messagebox.showwarning("Warning", "Both name and notes must be filled out.")
            return

        # Store the notes in the dictionary
        self.all_notes_dict[person_name] = notes

        # Add the name to the listbox
        self.names_listbox.insert(tk.END, person_name)

        # Clear input areas
        self.name_entry.delete(0, tk.END)
        self.notes_text.delete("1.0", tk.END)

    def save_all_notes(self):
        if not self.all_notes_dict:
            messagebox.showwarning("Warning", "Please add some notes first.")
            return

        # Ask for filename
        # filename = simpledialog.askstring("Filename", "Enter filename for the notes (without .md extension):")
        meeting_title = self.title_entry.get().strip()
        now = datetime.now()
        formated_date_slash = now.strftime('%m/%d/%Y')
        formated_date_underscore = now.strftime('%m_%d_%Y')
        filename = f'{meeting_title.replace(" ", "_")}_{formated_date_underscore}'
        file_path = os.path.join(os.path.dirname(get_exe_location()), "Notes/" + filename) + ".md"
        if not os.path.exists(os.path.dirname(get_exe_location()) + "/Notes"):
            os.mkdir(os.path.dirname(get_exe_location()) + "/Notes")
        if file_path:
            messagebox.showinfo('yeah', file_path)
            with open(f"{file_path}", "w") as file:
                # Writing the meeting title at the top
                messagebox.showinfo('yeah', "HERE")
                if meeting_title:
                    file.write(f"# Meeting: {meeting_title} -- {formated_date_slash}\n\n")
                file.write("## Individual Notes\n")
                for name, notes in self.all_notes_dict.items():
                    file.write(f"### {name}\n{notes}\n\n")
                additional_notes = self.additional_notes_text.get("1.0", tk.END).strip()
                file.write("## Additional Information\n{}".format(additional_notes))
                messagebox.showinfo('yeah', "HEREasdasdas")
            messagebox.showinfo("Saved", f"Notes saved to {meeting_title}_{formated_date_underscore}.md! at {os.path.dirname(get_exe_location()) + '/Notes'}")
            open_file_explorer(os.path.dirname(get_exe_location()) + "/Notes")
            # Clear the dictionary, input fields, and listbox
            self.all_notes_dict.clear()
            self.title_entry.delete(0, tk.END)  # Clear the meeting title
            self.name_entry.delete(0, tk.END)
            self.notes_text.delete("1.0", tk.END)
            self.additional_notes_text.delete("1.0", tk.END)
            self.names_listbox.delete(0, tk.END)


    def edit_note(self, event):
        selection = self.names_listbox.curselection()
        if len(selection) == 0:
            return
        index = selection[0]
        name = self.names_listbox.get(index)
        notes = self.all_notes_dict[name]

        editor_window = tk.Toplevel(self.root)
        editor_window.title(f"Editing {name}'s Notes")

        edit_name_frame = tk.Frame(editor_window)
        edit_name_frame.pack(pady=20)
        
        edit_name_label = tk.Label(edit_name_frame, text="Name:")
        edit_name_label.pack(side=tk.LEFT)
        
        edit_name_entry = tk.Entry(edit_name_frame, width=50)
        edit_name_entry.pack(side=tk.LEFT, padx=10)
        edit_name_entry.insert(0, name)

        edit_notes_frame = tk.Frame(editor_window)
        edit_notes_frame.pack(pady=20)
        
        edit_notes_label = tk.Label(edit_notes_frame, text="Notes:")
        edit_notes_label.pack(anchor=tk.W)
        
        edit_notes_text = scrolledtext.ScrolledText(edit_notes_frame, width=80, height=10)
        edit_notes_text.pack()
        edit_notes_text.insert(tk.END, notes)

        def save_edits():
            edited_name = edit_name_entry.get().strip()
            edited_notes = edit_notes_text.get("1.0", tk.END).strip()

            if not edited_name or not edited_notes:
                messagebox.showwarning("Warning", "Both name and notes must be filled out.")
                return

            # If the name is changed, update the name in the dictionary and listbox
            if edited_name != name:
                del self.all_notes_dict[name]
                self.names_listbox.delete(index)
                self.all_notes_dict[edited_name] = edited_notes
                self.names_listbox.insert(index, edited_name)
            else:
                self.all_notes_dict[edited_name] = edited_notes
            editor_window.destroy()
        save_edit_btn = tk.Button(editor_window, text="Save Edits", command=save_edits)
        save_edit_btn.pack(pady=20)

        editor_window.config(bg="gray35")
        edit_name_frame.config(bg="gray35")
        edit_notes_frame.config(bg="gray35")
        edit_name_entry.config(bg="gray45", fg="white")
        edit_notes_text.config(bg="gray45", fg="white")
        edit_name_label.config(bg="gray35", fg="white")
        edit_notes_label.config(bg="gray35", fg="white")
        save_edit_btn.config(bg="gray65", fg="white")


    def delete_selected_note(self, event):
        index = self.names_listbox.curselection()
        if index:
            index = index[0]
            name_to_delete = self.names_listbox.get(index)
            del self.all_notes_dict[name_to_delete]
            self.names_listbox.delete(index)
            # If backspace is the method of deletion, set the focus to the previous index (delete upward)
            if event.keysym == "BackSpace":
                self.names_listbox.selection_set(index - 1)
            # If delete is the method of deletion, set the focus to the next index (delete downward)
            if event.keysym == "Delete":
                self.names_listbox.selection_set(index)

def open_file_explorer(path="."):
    """
    Opens a file explorer window at the specified directory.

    Parameters:
    - path (str): The directory to open in the file explorer. Defaults to the current directory.
    """
    if not os.path.exists(path):
        print("The specified path does not exist.")
        return
    try:
        if platform.system() == "Windows":
            subprocess.Popen(['explorer', os.path.normpath(path)])
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(['open', path])
        else:  # Assume it's Linux or Unix
            subprocess.Popen(['xdg-open', path])
    except Exception as e:
        print(f"An error occurred: {e}")


def get_exe_location():
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller runtime, return the path to the .exe file
        return sys.executable
    else:
        # Regular Python runtime, return the current script's directory
        return os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    root = tk.Tk()
    app = MeetingNotesApp(root)
    root.mainloop()
