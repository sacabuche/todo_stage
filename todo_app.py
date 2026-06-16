import dearpygui.dearpygui as dpg

from storage import load_tasks, save_tasks
from theme import setup_theme

tasks = []
current_filter = "all"

dpg.create_context()
# setup_theme()


# ==========================
# STATISTIQUES
# ==========================

def update_stats():

    total = len(tasks)

    completed = sum(
        1 for t in tasks
        if t["completed"]
    )

    todo = total - completed

    percent = 0

    if total > 0:
        percent = completed / total

    dpg.set_value(
        "stat_total",
        f"Total : {total}"
    )

    dpg.set_value(
        "stat_done",
        f"Terminées : {completed}"
    )

    dpg.set_value(
        "stat_todo",
        f"À faire : {todo}"
    )

    dpg.set_value(
        "progress",
        percent
    )

    dpg.set_value(
        "progress_text",
        f"{int(percent * 100)}%"
    )


# ==========================
# AJOUT TACHE
# ==========================

def add_task():

    title = dpg.get_value("task_input")
    due = dpg.get_value("due_input")
    priority = dpg.get_value("priority_combo")

    if not title.strip():
        return

    tasks.append(
        {
            "title": title,
            "completed": False,
            "favorite": False,
            "priority": priority,
            "due_date": due
        }
    )

    save_tasks(tasks)

    dpg.set_value(
        "task_input",
        ""
    )

    rebuild_tasks()


# ==========================
# ACTIONS
# ==========================

def toggle_complete(sender, app_data, user_data):

    index = user_data

    tasks[index]["completed"] = app_data

    save_tasks(tasks)

    update_stats()


def toggle_favorite(sender, app_data, user_data):

    index = user_data

    tasks[index]["favorite"] = \
        not tasks[index]["favorite"]

    save_tasks(tasks)

    rebuild_tasks()


def delete_task(sender, app_data, user_data):

    index = user_data

    tasks.pop(index)

    save_tasks(tasks)

    rebuild_tasks()


# ==========================
# FILTRES
# ==========================

def set_filter(sender, app_data, user_data):

    global current_filter

    current_filter = user_data

    rebuild_tasks()


def task_visible(task):

    if current_filter == "all":
        return True

    if current_filter == "todo":
        return not task["completed"]

    if current_filter == "completed":
        return task["completed"]

    if current_filter == "favorites":
        return task["favorite"]

    return True


# ==========================
# REBUILD
# ==========================

def rebuild_tasks():

    dpg.delete_item(
        "task_container",
        children_only=True
    )

    for index, task in enumerate(tasks):

        if not task_visible(task):
            continue

        with dpg.group(
            horizontal=True,
            parent="task_container"
        ):

            dpg.add_checkbox(
                default_value=task["completed"],
                callback=toggle_complete,
                user_data=index
            )

            dpg.add_button(
                label="⭐" if task["favorite"] else "☆",
                callback=toggle_favorite,
                user_data=index
            )

            label = task["title"]

            if task["due_date"]:
                label += (
                    f" | {task['due_date']}"
                )

            label += (
                f" | {task['priority']}"
            )

            if task["priority"] == "High":
                color = (255, 80, 80)

            elif task["priority"] == "Medium":
                color = (255, 200, 0)

            else:
                color = (80, 220, 120)

            dpg.add_text(
                label,
                color=color
            )

            dpg.add_button(
                label="Supprimer",
                callback=delete_task,
                user_data=index
            )

    update_stats()


# ==========================
# INTERFACE
# ==========================

with dpg.window(
    label="Todo Manager Pro",
    width=1200,
    height=800
):

    with dpg.group(horizontal=True):

        # ----------------------
        # MENU GAUCHE
        # ----------------------

        with dpg.child_window(
            width=250
        ):  

            dpg.add_text("Navigation")

            dpg.add_button(
                label="📋 Toutes",
                callback=set_filter,
                user_data="all"
            )

            dpg.add_button(
                label="⏳À faire",
                callback=set_filter,
                user_data="todo"
            )

            dpg.add_button(
                label="✅Terminées",
                callback=set_filter,
                user_data="completed"
            )

            dpg.add_button(
                label="⭐Favoris",
                callback=set_filter,
                user_data="favorites"
            )

            dpg.add_separator()

            dpg.add_text(
                "Total : 0",
                tag="stat_total"
            )

            dpg.add_text(
                "Terminées : 0",
                tag="stat_done"
            )

            dpg.add_text(
                "À faire : 0",
                tag="stat_todo"
            )

            dpg.add_progress_bar(
                default_value=0,
                width=200,
                tag="progress"
            )
            with dpg.theme() as progress_theme:

                with dpg.theme_component(
                    dpg.mvProgressBar
                ):

                    dpg.add_theme_color(
                        dpg.mvThemeCol_PlotHistogram,
                        (0, 180, 255)
                    )

            dpg.bind_item_theme(
                "progress",
                progress_theme
            )

            dpg.add_text(
                "0%",
                tag="progress_text"
            )

        # ----------------------
        # ZONE PRINCIPALE
        # ----------------------

        with dpg.child_window():

            dpg.add_input_text(
                tag="task_input",
                hint="Nouvelle tâche..."
            )

            dpg.add_input_text(
                tag="due_input",
                hint="Date (2026-06-20)"
            )

            dpg.add_combo(
                [
                    "Low",
                    "Medium",
                    "High"
                ],
                default_value="Medium",
                tag="priority_combo"
            )

            dpg.add_button(
                label="Ajouter",
                callback=add_task
            )

            dpg.add_separator()

            dpg.add_child_window(
                tag="task_container"
            )


# ==========================
# DEMARRAGE
# ==========================

tasks = load_tasks()

rebuild_tasks()

dpg.create_viewport(
    title="Todo Manager Pro",
    width=1200,
    height=800
)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()