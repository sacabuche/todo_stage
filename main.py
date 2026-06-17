import dearpygui.dearpygui as dpg
import random
import os
import math

# ── Paleta ───────────────────────────────────────────────────────────────────
BG_MAIN        = (240, 235, 225, 255)
BG_CARD        = (250, 247, 241, 255)
BG_CARD_DONE   = (228, 222, 210, 255)
BG_CARD_PRIO   = (255, 250, 232, 255)
BG_HEADER      = (180, 120,  70, 255)
BG_INPUT       = (255, 252, 246, 255)
ACCENT         = (180, 120,  70, 255)
ACCENT_HOVER   = (200, 140,  90, 255)
ACCENT_ACTIVE  = (155,  98,  52, 255)
BTN_DEL        = (192,  85,  72, 255)
BTN_DEL_HOV    = (212, 105,  92, 255)
BTN_DEL_ACT    = (162,  65,  55, 255)
BTN_RND        = ( 82, 135, 105, 255)
BTN_RND_HOV    = (102, 155, 125, 255)
BTN_RND_ACT    = ( 62, 115,  85, 255)
BTN_CHK        = ( 70, 148,  86, 255)
BTN_CHK_HOV    = ( 90, 168, 106, 255)
BTN_CHK_ACT    = ( 50, 126,  66, 255)
BTN_UNDO       = (145, 132, 115, 255)
BTN_UNDO_HOV   = (165, 152, 135, 255)
BTN_UNDO_ACT   = (125, 112,  95, 255)
BTN_LANG       = ( 95, 120, 155, 255)
BTN_LANG_HOV   = (115, 140, 175, 255)
BTN_LANG_ACT   = ( 75, 100, 135, 255)
BTN_LANG_SEL   = ( 60,  95, 140, 255)
TEXT_WHITE     = (255, 255, 255, 255)
TEXT_DARK      = ( 55,  42,  28, 255)
TEXT_MID       = (118,  98,  72, 255)
TEXT_DONE      = (152, 138, 118, 255)
TEXT_PRIO      = (138,  85,  28, 255)
TEXT_HEADER    = (255, 240, 215, 200)
BORDER_CARD    = (215, 202, 182, 255)
BORDER_PRIO    = (210, 162,  55, 255)
CHECK_GREEN    = ( 70, 148,  86, 255)
STAR_GOLD      = (202, 152,  32, 255)

# ── Constantes de layout ──────────────────────────────────────────────────────
# Ancho total de la ventana
WIN_W         = 800
# Espacio ocupado a la izquierda del texto:
#   padding_card(10) + btn_chk/undo(~92) + spacer(3) + btn_del(28) + spacer(10) + icono(~28) + spacer(4) + padding_card(10)
TEXT_OFFSET_PX = 185   # píxeles ocupados antes del texto en la tarjeta
# Padding lateral del body (18 cada lado) + scrollbar (10) + border card (2*1)
BODY_PADDING_PX = 52
# Ancho disponible para el texto en píxeles
TEXT_WRAP_PX  = WIN_W - BODY_PADDING_PX - TEXT_OFFSET_PX   # ~563 px

# Altura de texto a 15px con interlineado DearPyGui (~19 px por linea)
LINE_H        = 19
# Altura base de tarjeta (padding vertical 8*2 + boton 28 + margen)
CARD_BASE_H   = 46
# Anchura de caracteres promedio a 15px ≈ 8.5 px/char
CHAR_W        = 8.5

# ── Traducciones ─────────────────────────────────────────────────────────────
LANGS = {
    "ES": {
        "title":         "Todo Stage",
        "subtitle":      "Organiza tu dia, una tarea a la vez.",
        "placeholder":   "Nueva tarea...",
        "btn_add":       "+ Anadir",
        "btn_random":    "  Prioridad aleatoria",
        "btn_del_done":  "  Borrar completadas",
        "counter":       "{total} tareas    {done} hechas    {pending} pendientes",
        "empty":         "Sin tareas aun  --  escribe una arriba y pulsa Anadir",
        "done_section":  "  Completadas",
        "btn_uncheck":   " Desmarcar ",
        "btn_check":     "  v  ",
        "btn_del_card":  " x ",
        "icon_done":     "(ok)",
        "icon_prio":     "(!)",
        "icon_normal":   "  o  ",
    },
    "FR": {
        "title":         "Todo Stage",
        "subtitle":      "Organisez votre journee, une tache a la fois.",
        "placeholder":   "Nouvelle tache...",
        "btn_add":       "+ Ajouter",
        "btn_random":    "  Priorite aleatoire",
        "btn_del_done":  "  Effacer terminees",
        "counter":       "{total} taches    {done} faites    {pending} en attente",
        "empty":         "Aucune tache  --  ecrivez ci-dessus et cliquez sur Ajouter",
        "done_section":  "  Terminees",
        "btn_uncheck":   " Decocher ",
        "btn_check":     "  v  ",
        "btn_del_card":  " x ",
        "icon_done":     "(ok)",
        "icon_prio":     "(!)",
        "icon_normal":   "  o  ",
    },
    "EN": {
        "title":         "Todo Stage",
        "subtitle":      "Organize your day, one task at a time.",
        "placeholder":   "New task...",
        "btn_add":       "+ Add",
        "btn_random":    "  Random priority",
        "btn_del_done":  "  Clear completed",
        "counter":       "{total} tasks    {done} done    {pending} pending",
        "empty":         "No tasks yet  --  type one above and click Add",
        "done_section":  "  Completed",
        "btn_uncheck":   " Uncheck ",
        "btn_check":     "  v  ",
        "btn_del_card":  " x ",
        "icon_done":     "(ok)",
        "icon_prio":     "(!)",
        "icon_normal":   "  o  ",
    },
}

# ── Estado ───────────────────────────────────────────────────────────────────
tasks: list[dict] = []
task_counter  = 0
current_lang  = "ES"
font_large    = None


# ── Fuentes ──────────────────────────────────────────────────────────────────
def find_fonts():
    if os.name == "nt":
        candidates = [
            ("C:/Windows/Fonts/segoeui.ttf",  "C:/Windows/Fonts/segoeuib.ttf"),
            ("C:/Windows/Fonts/arial.ttf",     "C:/Windows/Fonts/arialbd.ttf"),
        ]
    else:
        candidates = [
            ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
            ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
             "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
            ("/usr/share/fonts/truetype/freefont/FreeSans.ttf",
             "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"),
            ("/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
             "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf"),
        ]
    for normal, bold in candidates:
        if os.path.exists(normal):
            return normal, bold if os.path.exists(bold) else normal
    return None, None


def T(key: str, **kw) -> str:
    text = LANGS[current_lang].get(key, key)
    return text.format(**kw) if kw else text


# ── Temas ────────────────────────────────────────────────────────────────────
def apply_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg,       BG_MAIN)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg,        BG_MAIN)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg,        BG_INPUT)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (255, 253, 248, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive,  (245, 240, 230, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text,           TEXT_DARK)
            dpg.add_theme_color(dpg.mvThemeCol_Border,         BORDER_CARD)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg,    BG_MAIN)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab,  BORDER_CARD)
            dpg.add_theme_color(dpg.mvThemeCol_Button,         ACCENT)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,  ACCENT_HOVER)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,   ACCENT_ACTIVE)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,  7)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding,  9)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding,   10, 7)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing,    8, 5)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding,  0, 0)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize,  8)
    dpg.bind_theme(global_theme)


def make_btn_theme(base, hover, active, radius=7):
    with dpg.theme() as t:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button,        base)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, hover)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,  active)
            dpg.add_theme_color(dpg.mvThemeCol_Text,          TEXT_WHITE)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, radius)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding,  5, 5)
    return t


def make_card_theme(bg, border):
    with dpg.theme() as t:
        with dpg.theme_component(dpg.mvChildWindow):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, bg)
            dpg.add_theme_color(dpg.mvThemeCol_Border,  border)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding,  9)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding,  10, 8)
    return t


def make_text_theme(color):
    with dpg.theme() as t:
        with dpg.theme_component(dpg.mvText):
            dpg.add_theme_color(dpg.mvThemeCol_Text, color)
    return t


# ── Calculo de altura de tarjeta ─────────────────────────────────────────────
def estimate_card_height(text: str) -> int:
    """
    Estima cuantas lineas ocupara el texto usando el ancho de wrap en pixeles,
    y devuelve la altura total de la tarjeta.
    DearPyGui usa wrap= en pixeles para cortar lineas automaticamente.
    Aproximamos cuantos caracteres caben en TEXT_WRAP_PX px a CHAR_W px/char.
    """
    chars_per_line = max(1, int(TEXT_WRAP_PX / CHAR_W))
    # Contar lineas manualmente para estimar (solo para la altura)
    words = text.split()
    lines = 1
    current_len = 0
    for word in words:
        wlen = len(word)
        if current_len == 0:
            current_len = wlen
        elif current_len + 1 + wlen <= chars_per_line:
            current_len += 1 + wlen
        else:
            lines += 1
            current_len = wlen
    extra = max(0, lines - 1) * LINE_H
    return CARD_BASE_H + extra


# ── Contador ──────────────────────────────────────────────────────────────────
def update_counter():
    total   = len(tasks)
    done    = sum(1 for t in tasks if t["done"])
    pending = total - done
    dpg.set_value("counter_text", T("counter", total=total, done=done, pending=pending))


# ── Render ────────────────────────────────────────────────────────────────────
def render_tasks():
    for child in dpg.get_item_children("task_list_group", slot=1) or []:
        dpg.delete_item(child)

    if not tasks:
        dpg.add_spacer(height=16, parent="task_list_group")
        t = dpg.add_text(T("empty"), parent="task_list_group")
        dpg.bind_item_theme(t, make_text_theme(TEXT_MID))
        update_counter()
        return

    pending   = [t for t in tasks if not t["done"]]
    completed = [t for t in tasks if t["done"]]
    ordered   = pending + completed

    th_del   = make_btn_theme(BTN_DEL,  BTN_DEL_HOV,  BTN_DEL_ACT,  radius=16)
    th_chk   = make_btn_theme(BTN_CHK,  BTN_CHK_HOV,  BTN_CHK_ACT,  radius=16)
    th_undo  = make_btn_theme(BTN_UNDO, BTN_UNDO_HOV, BTN_UNDO_ACT, radius=7)

    th_txt_done = make_text_theme(TEXT_DONE)
    th_txt_dark = make_text_theme(TEXT_DARK)
    th_txt_prio = make_text_theme(TEXT_PRIO)

    th_card_normal = make_card_theme(BG_CARD,      BORDER_CARD)
    th_card_done   = make_card_theme(BG_CARD_DONE, BORDER_CARD)
    th_card_prio   = make_card_theme(BG_CARD_PRIO, BORDER_PRIO)

    shown_done_hdr = False

    for task in ordered:

        # Cabecera de seccion completadas
        if task["done"] and not shown_done_hdr and pending:
            dpg.add_spacer(height=8, parent="task_list_group")
            sep = dpg.add_text(T("done_section"), parent="task_list_group")
            dpg.bind_item_theme(sep, make_text_theme(TEXT_DONE))
            dpg.add_spacer(height=4, parent="task_list_group")
            shown_done_hdr = True

        real_idx = tasks.index(task)
        card_tag = f"card_{task['tag']}"
        avail_w  = (dpg.get_item_width("task_scroll") or WIN_W) - 22
        h        = estimate_card_height(task["text"])

        # Tarjeta
        with dpg.child_window(
            tag=card_tag,
            parent="task_list_group",
            width=avail_w,
            height=h,
            border=True,
            no_scrollbar=True,
        ):
            if task["done"]:
                dpg.bind_item_theme(card_tag, th_card_done)
            elif task.get("priority"):
                dpg.bind_item_theme(card_tag, th_card_prio)
            else:
                dpg.bind_item_theme(card_tag, th_card_normal)

            with dpg.group(horizontal=True):

                # Boton check / desmarcar
                if task["done"]:
                    u_tag = f"undo_{task['tag']}"
                    dpg.add_button(
                        label=T("btn_uncheck"),
                        tag=u_tag,
                        callback=lambda s, a, u: toggle_done(u),
                        user_data=real_idx,
                        width=92, height=28,
                    )
                    dpg.bind_item_theme(u_tag, th_undo)
                else:
                    c_tag = f"chk_{task['tag']}"
                    dpg.add_button(
                        label=T("btn_check"),
                        tag=c_tag,
                        callback=lambda s, a, u: toggle_done(u),
                        user_data=real_idx,
                        width=32, height=28,
                    )
                    dpg.bind_item_theme(c_tag, th_chk)

                dpg.add_spacer(width=3)

                # Boton borrar
                d_tag = f"del_{task['tag']}"
                dpg.add_button(
                    label=T("btn_del_card"),
                    tag=d_tag,
                    callback=lambda s, a, u: delete_task(u),
                    user_data=real_idx,
                    width=28, height=28,
                )
                dpg.bind_item_theme(d_tag, th_del)

                dpg.add_spacer(width=10)

                # Icono de estado
                if task["done"]:
                    ico = dpg.add_text(T("icon_done"))
                    dpg.bind_item_theme(ico, make_text_theme(CHECK_GREEN))
                elif task.get("priority"):
                    ico = dpg.add_text(T("icon_prio"))
                    dpg.bind_item_theme(ico, make_text_theme(STAR_GOLD))
                else:
                    ico = dpg.add_text(T("icon_normal"))
                    dpg.bind_item_theme(ico, make_text_theme(TEXT_MID))

                dpg.add_spacer(width=4)

                # ── Texto con wrap nativo en pixeles ──────────────────────────
                # wrap=TEXT_WRAP_PX le dice a DearPyGui exactamente cuantos
                # pixeles de ancho tiene el texto antes de saltar de linea.
                t_tag = f"txt_{task['tag']}"
                dpg.add_text(task["text"], tag=t_tag, wrap=TEXT_WRAP_PX)
                if task["done"]:
                    dpg.bind_item_theme(t_tag, th_txt_done)
                elif task.get("priority"):
                    dpg.bind_item_theme(t_tag, th_txt_prio)
                else:
                    dpg.bind_item_theme(t_tag, th_txt_dark)

        dpg.add_spacer(height=5, parent="task_list_group")

    update_counter()


# ── Callbacks ─────────────────────────────────────────────────────────────────
def add_task(sender=None, app_data=None, user_data=None):
    global task_counter
    raw = dpg.get_value("input_task").strip()
    if not raw:
        return
    task_counter += 1
    tasks.append({"text": raw, "done": False, "priority": False,
                  "tag": f"t{task_counter}"})
    dpg.set_value("input_task", "")
    render_tasks()


def delete_task(idx: int):
    if 0 <= idx < len(tasks):
        tasks.pop(idx)
        render_tasks()


def toggle_done(idx: int):
    if 0 <= idx < len(tasks):
        tasks[idx]["done"]     = not tasks[idx]["done"]
        tasks[idx]["priority"] = False
        render_tasks()


def delete_done(sender=None, app_data=None, user_data=None):
    tasks[:] = [t for t in tasks if not t["done"]]
    render_tasks()


def promote_random(sender=None, app_data=None, user_data=None):
    pending = [t for t in tasks if not t["done"]]
    if not pending:
        return
    for t in tasks:
        t["priority"] = False
    chosen = random.choice(pending)
    chosen["priority"] = True
    tasks.remove(chosen)
    tasks.insert(0, chosen)
    render_tasks()


def change_lang(sender=None, app_data=None, user_data=None):
    global current_lang
    new_lang = user_data
    if new_lang == current_lang:
        return
    current_lang = new_lang
    rebuild_ui()


# ── Rebuild de UI (para cambio de idioma) ─────────────────────────────────────
def rebuild_ui():
    if dpg.does_item_exist("main_win"):
        dpg.delete_item("main_win")
    build_ui()
    dpg.set_item_width("main_win",  WIN_W)
    dpg.set_item_height("main_win", 640)
    dpg.set_item_pos("main_win",  [0, 0])


# ── UI ────────────────────────────────────────────────────────────────────────
def build_ui():
    th_del      = make_btn_theme(BTN_DEL,  BTN_DEL_HOV,  BTN_DEL_ACT)
    th_rnd      = make_btn_theme(BTN_RND,  BTN_RND_HOV,  BTN_RND_ACT)
    th_lang     = make_btn_theme(BTN_LANG,     BTN_LANG_HOV, BTN_LANG_ACT, radius=5)
    th_lang_sel = make_btn_theme(BTN_LANG_SEL, BTN_LANG_HOV, BTN_LANG_ACT, radius=5)

    with dpg.window(
        tag="main_win",
        no_title_bar=True,
        no_resize=True,
        no_move=True,
        no_scrollbar=True,
        no_scroll_with_mouse=True,
    ):

        # ── Cabecera ─────────────────────────────────────────────────────────
        with dpg.child_window(height=78, border=False, tag="header"):
            with dpg.theme() as hdr_theme:
                with dpg.theme_component(dpg.mvChildWindow):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, BG_HEADER)
                    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 20, 10)
            dpg.bind_item_theme("header", hdr_theme)

            with dpg.group(horizontal=True):
                with dpg.group():
                    title = dpg.add_text(T("title"))
                    with dpg.theme() as t_title:
                        with dpg.theme_component(dpg.mvText):
                            dpg.add_theme_color(dpg.mvThemeCol_Text, TEXT_WHITE)
                    dpg.bind_item_theme(title, t_title)
                    if font_large:
                        dpg.bind_item_font(title, font_large)

                    sub = dpg.add_text(T("subtitle"))
                    with dpg.theme() as t_sub:
                        with dpg.theme_component(dpg.mvText):
                            dpg.add_theme_color(dpg.mvThemeCol_Text, TEXT_HEADER)
                    dpg.bind_item_theme(sub, t_sub)

                # Botones de idioma alineados a la derecha
                dpg.add_spacer(width=10)
                with dpg.group(horizontal=True):
                    for code, label in [("ES", " ES "), ("FR", " FR "), ("EN", " EN ")]:
                        btn = dpg.add_button(
                            label=label,
                            callback=change_lang,
                            user_data=code,
                            width=38, height=24,
                        )
                        dpg.bind_item_theme(
                            btn,
                            th_lang_sel if code == current_lang else th_lang
                        )
                    dpg.add_spacer(width=4)

        # ── Cuerpo ───────────────────────────────────────────────────────────
        with dpg.child_window(border=False, autosize_y=True, no_scrollbar=True):
            with dpg.theme() as body_theme:
                with dpg.theme_component(dpg.mvChildWindow):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, BG_MAIN)
                    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 18, 14)
            dpg.bind_item_theme(dpg.last_item(), body_theme)

            # Campo de entrada
            with dpg.group(horizontal=True):
                dpg.add_input_text(
                    tag="input_task",
                    hint=T("placeholder"),
                    width=-162,
                    height=36,
                    on_enter=True,
                    callback=add_task,
                )
                dpg.add_spacer(width=6)
                dpg.add_button(
                    label=T("btn_add"),
                    callback=add_task,
                    width=148, height=36,
                )

            dpg.add_spacer(height=8)

            # Botones secundarios
            with dpg.group(horizontal=True):
                b1 = dpg.add_button(
                    label=T("btn_random"),
                    callback=promote_random,
                    width=205, height=30,
                )
                dpg.bind_item_theme(b1, th_rnd)
                dpg.add_spacer(width=8)
                b2 = dpg.add_button(
                    label=T("btn_del_done"),
                    callback=delete_done,
                    width=200, height=30,
                )
                dpg.bind_item_theme(b2, th_del)

            dpg.add_spacer(height=10)

            # Contador
            ctr = dpg.add_text(
                T("counter", total=0, done=0, pending=0),
                tag="counter_text",
            )
            dpg.bind_item_theme(ctr, make_text_theme(TEXT_MID))

            dpg.add_spacer(height=8)

            # Lista scrollable
            with dpg.child_window(tag="task_scroll", border=False, autosize_y=True):
                with dpg.theme() as scroll_theme:
                    with dpg.theme_component(dpg.mvChildWindow):
                        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, BG_MAIN)
                        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 2, 4)
                dpg.bind_item_theme("task_scroll", scroll_theme)

                with dpg.group(tag="task_list_group"):
                    t = dpg.add_text(T("empty"))
                    dpg.bind_item_theme(t, make_text_theme(TEXT_MID))


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    global font_large

    dpg.create_context()
    apply_theme()

    font_normal_path, font_bold_path = find_fonts()
    with dpg.font_registry():
        if font_normal_path:
            try:
                dpg.add_font(font_normal_path, 15, default_font=True)
                font_large = dpg.add_font(font_bold_path, 22)
            except Exception as e:
                print(f"Fuente no cargada: {e}")
                font_large = None
        else:
            font_large = None

    build_ui()

    dpg.create_viewport(title="Todo Stage", width=WIN_W, height=640, resizable=False)
    dpg.set_viewport_clear_color(list(BG_MAIN))
    dpg.setup_dearpygui()
    dpg.show_viewport()

    dpg.set_item_width("main_win",  WIN_W)
    dpg.set_item_height("main_win", 640)
    dpg.set_item_pos("main_win",  [0, 0])

    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()