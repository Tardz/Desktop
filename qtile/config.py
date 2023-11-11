### CONF IMPORTS ###
from libqtile.config import Screen
from libqtile import hook, bar
from libqtile.lazy import lazy
import subprocess
import os
import re

### KEYBINDING AND GROUPS IMPORTS ###
from libqtile.config import Match, Key, KeyChord, Click, Drag, ScratchPad, Group, DropDown
from libqtile import qtile as Qtile
import subprocess

### BAR IMPORTS ###
from qtile_extras.widget.decorations import BorderDecoration, RectDecoration
from libqtile.widget.bluetooth import Bluetooth
from libqtile.widget.sep import Sep
from libqtile.widget import base
from qtile_extras import widget
from libqtile.bar import Bar
from libqtile import bar   

### LAYOUT IMPORTS ###
from libqtile.layout.floating import Floating
from libqtile.layout.xmonad import MonadTall
from libqtile.layout.stack import Stack

### SETTINGS ###
from settings import *

### LAZY FUNCTIONS ###
@lazy.function
def move_focus_and_mouse(qtile, monitor = 0):
    qtile.cmd_to_screen(monitor)
    if monitor == 0:
        qtile.cmd_spawn("xdotool mousemove 950 500")
    elif monitor == 1:
        qtile.cmd_spawn("xdotool mousemove 2900 500")

@lazy.function
def spawn_alttab_once(qtile):
    if not alttab_spawned:
        qtile.cmd_spawn('alttab -bg "#2e3440" -fg "#d8dee9" -bc "#2e3440" -bw 15 -inact "#3b4252" -frame "#81a1c1"')

@lazy.function
def check(qtile, app, group, command = ""):
    qtile.cmd_spawn(["/home/jonalm/scripts/qtile/check_and_launch_app.py", app, group, command])

@lazy.function
def close_all_windows(qtile):
    for group in qtile.groups:
        for window in group.windows:
            window.kill()

@lazy.function
def get_next_screen_group(qtile):
    subprocess.call(["qtile", "cmd-obj", "-o", "cmd", "-f", "next_screen"])

    data = subprocess.check_output(["qtile", "cmd-obj", "-o", "group", "-f", "info"]).decode().strip()

    match = re.search(r"'name': '(\d+)'", data)

    if match:
        next_screen_group = match.group(1)
        return next_screen_group
    else:
        print("group not found. Error: ", match)
        
    # return subprocess.check_output(["python ", "/home/jonalm/.config/qtile/qtile_scripts/get_next_screen_group.py"]).decode()
    # return qtile.cmd_spawn("python /home/jonalm/.config/qtile/qtile_scripts/get_next_screen_group.py")

### KEYBINDINGS ###
#- KEYS_START
keys = [
        #--[ESSENTIALS]--#
        # Screen reset: lazy.spawn("/home/jonalm/scripts/term/reset_screens.sh")
        Key([mod], "Tab", lazy.next_layout(), desc='Toggle through layouts'),
        Key([mod], "q", lazy.window.kill(), desc='Kill active window'),
        Key([mod, "shift"], "r", lazy.restart(), desc='Restart Qtile'),
        Key([mod, "shift"], "q", lazy.shutdown(), desc='Shutdown Qtile'),
        Key([mod, "control"], "q", close_all_windows, desc='Close all windows'),
        KeyChord([mod], "x", [
            Key([], "u", lazy.spawn("sudo systemctl poweroff")),
            Key([], "s", lazy.spawn("sudo systemctl suspend")),
            Key([], "r", lazy.spawn("sudo systemctl reboot"))
        ]),
        
        #- -[AUDIO]--#
        # Key([], 'XF86AudioMute', lazy.spawn('ponymix toggle')),
        # Key([], 'XF86AudioRaiseVolume', lazy.spawn('ponymix increase 5')),
        # Key([], 'XF86AudioLowerVolume', lazy.spawn('ponymix decrease 5')),
        # Key([], 'XF86AudioPlay', lazy.spawn(music_cmd + 'PlayPause')),
        # Key([], 'XF86AudioNext', lazy.function(next_prev('Next'))),
        # Key([], 'XF86AudioPrev', lazy.function(next_prev('Previous'))),

        #--[SWITCH MONITOR FOCUS AND GROUPS]--#
        Key(["control"], "Tab", spawn_alttab_once, desc='alttab'),
        Key([mod], "Right", lazy.screen.next_group(), desc='Next group right'),
        Key([mod], "Left", lazy.screen.prev_group(), desc='Next group left'),

        #--[WINDWOW CONTROLS]--#
        Key([mod], "Down", lazy.layout.down(), desc='Move focus down in current stack pane'),
        Key([mod], "Up", lazy.layout.up(), desc='Move focus up in current stack pane'),
        Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), lazy.layout.section_down(), desc='Move windows down in current stack'),
        Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), lazy.layout.section_up(), desc='Move windows up in current stack'),
        Key([mod, "control"], "Left", lazy.layout.shrink(), lazy.layout.decrease_nmaster(), desc='Shrink window'),
        Key([mod, "control"], "Right", lazy.layout.grow(), lazy.layout.increase_nmaster(), desc='Expand window'),
        Key([mod, "control"], "Down", lazy.layout.normalize(), desc='Normalize window size ratios'),
        Key([mod, "control"], "Up", lazy.layout.maximize(), desc='Toggle window between minimum and maximum sizes'),
        Key([mod], "f", lazy.window.toggle_floating(), desc='Toggle floating'),
        Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), desc='Toggle fullscreen'),
        Key([mod], "z", lazy.window.toggle_minimize(), lazy.group.next_window(), desc='Minimize window'),

        #--[APPS]--#
        Key([mod], "c", move_focus_and_mouse(1), lazy.group["1"].toscreen(), check("brave", "1"), desc='Browser'),
        Key([mod], "e", lazy.spawn("java /home/jonalm/my_projects/Budgeting_app/src/main/java/com/example/budgeting_app/Main.java"), desc='Browser'),
        Key([mod], "n", move_focus_and_mouse(1), lazy.group["3"].toscreen(), check("ranger", "3", "alacritty --title ranger -e"), desc='Filemanager'),
        Key([mod], "d", move_focus_and_mouse(1), lazy.group["4"].toscreen(), check("discord", "4"), desc='Discord'),
        Key([mod], "v", move_focus_and_mouse(0), lazy.group["2"].toscreen(), desc='Code'),
        Key([mod], "m", move_focus_and_mouse(1), lazy.group["3"].toscreen(), check("thunderbird", "3"), desc='Mail'),
        Key([mod], "g", move_focus_and_mouse(0), lazy.group["4"].toscreen(), check("steam", "4"), desc='Steam'),
        Key([mod], "o", lazy.group["4"].toscreen(), desc='Libre office'),
        Key([], "XF86AudioRaiseVolume", lazy.spawn("/home/jonalm/scripts/other/get_notifications.py"), desc='Libre office'),
        
        #--[URLS]--#
        Key([mod], "y", move_focus_and_mouse(1), lazy.group["1"].toscreen(), check("youtube.com", "1", "brave"), desc='Youtube'),

        #--[TERM]--#
        Key([mod], "h", move_focus_and_mouse(0), lazy.group["3"].toscreen(), check("htop", "3", "alacritty --title htop -e"), desc='Htop'),
        Key([mod], "plus", lazy.spawn("/home/jonalm/scripts/term/show_keys.sh"), desc='Keybindings'),

        #--[ROFI]--#
        Key([mod], "space", lazy.spawn("/home/jonalm/.config/rofi/files/launchers/type-1/launcher.sh"), desc='Rofi drun'),
        Key([mod], "Escape", lazy.spawn("/home/jonalm/.config/rofi/files/powermenu/type-2/powermenu.sh"), desc='Rofi powermenu'),
        Key([mod], "w", lazy.spawn("/home/jonalm/scripts/rofi/config/config_files.sh"), desc='Rofi config files'),
        Key([mod], "l", lazy.spawn("/home/jonalm/scripts/rofi/search/search_web.sh"), desc='Rofi web search'),
        Key([mod], "k", lazy.spawn("/home/jonalm/scripts/rofi/automation/automation.sh"), desc='Rofi automation scripts'),
#- KEYS_END
]
        
### GROUP SETTINGS ###
#CIRCLE: 
### GROUP SETTINGS ###
groups = [
        Group('1', label = "", matches=[ #Browser
            Match(wm_class = ["chromium"]),
            Match(wm_class = ["brave-browser"]),
                ]), 
        Group('2', label = "", matches=[ #Code
            Match(wm_class = ["code"]),
            Match(wm_class = ["jetbrains-clion"]),
            Match(wm_class = ["jetbrains-studio"]),
            Match(wm_class = ["jetbrains-idea"]),
            ]), 
        Group('3', label = "", matches=[ #Files
            Match(wm_class = ["pcmanfm"]),
            Match(wm_class = ["thunderbird"]),
            Match(wm_class = ["lxappearance"]),
            Match(wm_class = ["tlpui"]),
            ]), 
        Group('4', label = "", matches=[ #Social
            Match(wm_class = ["discord"]),
            ]), 
        Group('9', label = ""), #Scratchpad

]

focus_value = True

### SCRATCHPAD ###
groups.append(ScratchPad('9', [
    DropDown('terminal', 'alacritty', warp_pointer=True, width=0.34, height=0.5, x=0.33, y=0.2, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('mixer', 'pavucontrol', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('net', 'nm-connection-editor', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('bluetooth', 'blueman-manager', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('filemanager', 'pcmanfm', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = focus_value),
    DropDown('music', 'spotify', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('todo', 'ticktick', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = focus_value),
    DropDown('passwords', '/home/jonalm/.webcatalog/LastPass/LastPass', warp_pointer=True, width=0.5, height=0.5, x=0.2, y=0.12, opacity=1, on_focus_lost_hide = focus_value),
]))

### MOVE WINDOW TO WORKSPACE AND DROPDOWNS ###
for i in groups:
    keys.extend([
#- SCRATCHPAD_KEYS_START

        #--[WINDOWS]--#
        Key([mod, "shift"], "Left", lazy.window.togroup(get_next_screen_group), desc="move focused window to group {}".format(i.name)),
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name)),
        #--[SCRATCHPAD]--#
        Key([mod], "Return", lazy.group['9'].dropdown_toggle('terminal'), desc='Terminal'),
        Key([mod], "period", lazy.group['9'].dropdown_toggle('mixer'), desc='Volume'),
        Key([mod], "minus", lazy.group['9'].dropdown_toggle('net'), desc='Wifi'),
        Key([mod], "comma", lazy.group['9'].dropdown_toggle('bluetooth'), desc='Bluetooth'),
        Key([mod], "s", lazy.group['9'].dropdown_toggle('music'), desc='Spotify'),
        Key([mod], "r", lazy.group['9'].dropdown_toggle('todo'), desc='Ticktick'), 
        Key([mod], "p", lazy.group['9'].dropdown_toggle('passwords'), desc='Lastpass'),
#- SCRATCHPAD_KEYS_END
    ])

### DRAG FLOATING LAYOUTS ###
@lazy.function
def drag_and_snap_to_tile(qtile):
    # Snap the window to the tile layout when you release the mouse button
    qtile.current_window.toggle_floating()

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
    ]
### CUSTOM WIDGETS ###
def seperator(custom_padding = seperator_padding):
    return Sep(
        linewidth    = seperator_line_width,
        foreground   = bar_background_color,
        padding      = custom_padding,
        size_percent = 0,
    )

def left_decor(color: str, padding_x=None, padding_y=5, round=False):
    radius = 4 if round else [4, 0, 0, 4]
    return [
        RectDecoration(
            colour=color,
            radius=radius,
            filled=True,
            padding_x=padding_x,
            padding_y=padding_y,
        )
    ]


def right_decor(round=False, padding_x=0, padding_y=5):
    radius = 4 if round else [0, 4, 4, 0]
    return [
        RectDecoration(
            colour=bar_border_color,
            radius=radius,
            filled=True,
            padding_y=padding_y,
            padding_x=padding_x,
        )
    ]

class WifiSsidWidget(widget.TextBox, base.InLoopPollText):
    def __init__(self):
        base.InLoopPollText.__init__(
            self, 
            update_interval = wifi_update_interval,
            font            = bold_font,
            padding         = widget_default_padding,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("alacritty -e nmtui")},
            decorations     = right_decor(True)
        )
        
    def poll(self):
        ssid = subprocess.check_output(['python3', '/home/jonalm/scripts/qtile/get_wifi_ssid.py'], text=True).strip()
        if ssid == "lo":
            return "Disconnected"
        elif ssid == "Wired connection 1":
            return "Ethernet"
        else:
            return ssid
        
class NotificationWidget(widget.TextBox, base.InLoopPollText):
    def __init__(self):
        base.InLoopPollText.__init__(
            self, 
            update_interval = wifi_update_interval,
            font            = bold_font,
            padding         = widget_default_padding,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("/home/jonalm/scripts/other/get_notifications.py")},
            max_chars       = 10,
            decorations     = right_decor(True)
        )
        
    def poll(self):
        notification_message = subprocess.check_output(['/home/jonalm/scripts/other/get_recent_urgent_notification.py'], text=True).strip()
        if notification_message:
            return notification_message

### WIDGET SETTINGS ###
widget_defaults = dict(
    font        = bold_font,
    fontsize    = widget_default_font_size + 2,
    padding     = widget_default_padding,
    foreground  = widget_default_foreground_color,
)

group_box_settings = {
        "margin"                      : groupbox_margin,
        "font"                        : icon_font,
        "highlight_method"            : "block",
        "borderwidth"                 : 6,
        "rounded"                     : True,
        "disable_drag"                : True,
        "active"                      : bar_border_color,
        "inactive"                    : bar_background_color,
        "block_highlight_text_color"  : "#000000",
        "highlight_color"             : "#000000",
        "this_current_screen_border"  : "#81A1C1",
        "hide_unused"                 : True,
        "other_current_screen_border" : group_box_other_border_color,
        "this_screen_border"          : group_box_this_border_color,
        "other_screen_border"         : group_box_other_border_color,
        "foreground"                  : group_box_foreground_color,
        # "background"                  : group_box_background_color,
        "urgent_border"               : group_box_urgentborder_color,
}

### BAR ###
top_bar_1 = Bar([
    seperator(icon_seperator_padding - 2),
    widget.TextBox(        
        text        = f"<span font='Font Awesome 6 free solid {widget_default_font_size}' foreground='#000000' size='medium'></span>",
        mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/main_menu.py")},
        decorations = left_decor(round = True, color = battery_icon_color),
    ),

    seperator(icon_seperator_padding),
    widget.CurrentLayoutIcon(
        custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
        scale             = layouticon_scale,
        decorations       = left_decor(round = True, color = cpu_icon_color),
    ),
    
    # GROUPBOX #
    seperator(icon_seperator_padding),
    widget.GroupBox(
        **group_box_settings,
        decorations = left_decor(round = True, color = wifi_icon_color),
    ),

    seperator(icon_seperator_padding),
    widget.TextBox(        
        text        = f"<span font='Font Awesome 6 free solid {widget_default_font_size}' foreground='#000000' size='medium'></span>",
        # mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/main_menu.py")},
        decorations = left_decor(round = True, color = "#b48ead"),
    ),

    seperator(icon_seperator_padding - 4),
    widget.TaskList(
        font                = "FiraCode Nerd Font Bold",
        fontsize            = widget_default_font_size + 2,
        padding_y           = widget_default_padding,
        margin              = 2,
        borderwidth         = 6,
        spacing             = 2,
        txt_floating        = ' 缾 ',
        txt_maximized       = ' 类 ',
        txt_minimized       = ' 絛 ',
        title_width_method  = "uniform",
        urgent_alert_method = "border",
        highlight_method    = 'block',
        border              = bar_border_color,
        unfocused_border    = "#3c4455",
    ),
    seperator(icon_seperator_padding - 6),
], bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

top_bar_2 = Bar([
    seperator(icon_seperator_padding - 6),
    widget.TaskList(
        font                = "FiraCode Nerd Font Bold",
        fontsize            = widget_default_font_size + 2,
        padding_y           = widget_default_padding,
        margin              = 2,
        borderwidth         = 6,
        spacing             = 2,
        txt_floating        = ' 缾 ',
        txt_maximized       = ' 类 ',
        txt_minimized       = ' 絛 ',
        title_width_method  = "uniform",
        urgent_alert_method = "border",
        highlight_method    = 'block',
        border              = bar_border_color,
        unfocused_border    = "#3c4455",
    ),
    seperator(icon_seperator_padding - 4),

    #  WIFI #
    widget.TextBox(        
        text            = f"<span font='Font Awesome 6 free solid {widget_default_font_size}' foreground='#000000' size='medium'></span>",
        foreground      = notification_history_icon_color,
        mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/wifi_menu.py")},
        decorations     = left_decor(wifi_icon_color, round = True),
    ),
    WifiSsidWidget(),

    # CPU #
    seperator(icon_seperator_padding),
    widget.TextBox(        
        text        = f"<span font='Font Awesome 6 free solid {widget_default_font_size}' foreground='#000000'size='medium'></span>",
        mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/cpu_stats_menu.py")},
        decorations = left_decor(cpu_icon_color, round = True),
    ),
    widget.CPU(
        format          = "{load_percent}%",
        markup          = True,
        update_interval = cpu_update_interval,
        mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("alacritty -e sudo auto-cpufreq --stats")},
        decorations     = right_decor(True),
    ),    
    
    # URGENT NOTIFICATION #
    seperator(icon_seperator_padding),
    widget.TextBox(        
        text        = f"<span font='Font Awesome 6 free solid {widget_default_font_size}' foreground='#000000' size='medium'></span>",
        decorations = left_decor(notification_icon_color, round = True),
    ),
    NotificationWidget(),
    
    # DATE #
    seperator(icon_seperator_padding),
    widget.TextBox(        
        text        = f"<span font='Font Awesome 6 free solid {widget_default_font_size}' foreground='#000000'size='medium'></span>",
        decorations = left_decor(date_icon_color, round = True),
    ),
    widget.Clock(
        format      = "%a %b %d",
        markup      = True,
        decorations = right_decor(True),
    ),

    # TIME #
    seperator(icon_seperator_padding),
    widget.Clock(
        format      = "%R",
        fontsize    = widget_default_font_size + 3,
        decorations = right_decor(True),
    ),
    seperator(icon_seperator_padding - 2),
], bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

### LAYOUT SETTINGS ###
layouts = [
    MonadTall(
        border_normal       = layout_normal_color_monadtall,
        border_focus        = layout_focus_color_monadtall,
        margin              = layout_margin,
        single_margin       = layout_margin,
        border_width        = layout_border_width,
        single_border_width = layout_border_width,
    ),
    Stack(
        border_normal       = layout_normal_color_stack,
        border_focus        = layout_focus_color_stack,
        margin              = layout_margin,
        num_stacks          = layout_num_stacks,
        border_width        = layout_border_width,
    )
]

### FLOATING LAYOUT SETTINGS AND ASSIGNED APPS ###
floating_layout = Floating(
    border_normal = layout_normal_color_floating,
    border_focus  = layout_focus_color_floating,
    border_width  = floating_border_width,
    float_rules   = [
        ###Insert here###
        *Floating.default_float_rules,
        Match(wm_class = "blueman-manager"),
        Match(wm_class = "arandr"),
        Match(wm_class = "cairo-dock"),
        Match(wm_class = "gpick"),
        Match(wm_class = "com.example.budgeting_app.Main"),
        Match(wm_class = "com.example.budgeting_app.HelloApplication"),
        Match(wm_class = "yad"),
        Match(wm_class = "nitrogen"),
        Match(wm_class = "se-liu-jonal155-tetris-Tester"),
        Match(wm_class = "qalculate-gtk"),
        Match(wm_class = "pavucontrol"),
        Match(wm_class = "blueman-manager"),
        Match(wm_class = "polychromatic-controller"),
        Match(wm_class = "qalculate-qt"),
        Match(wm_class = "lxappearance"),
        Match(wm_class = "se-liu-davhe786_jonal155-pong-Main"),
        ])

### DECLARING WIDGET SETTINGS ###
extension_defaults = widget_defaults.copy()

### DECLARING PANEL ###
# subprocess.call(["nitrogen", "--restore", "&"])
screen_output = subprocess.check_output(["xrandr", "-q"]).decode().strip()
screen_data = subprocess.check_output(['awk', '/DisplayPort-0|DisplayPort-2/ {print $1 ": " $2}'], input=screen_output.encode()).decode().strip()
if "DisplayPort-0: connected" and "DisplayPort-2: connected" in screen_data:
    single_monitor = False
    top_bar_1_var  = top_bar_1
    top_bar_2_var  = top_bar_2
else:
    top_bar_1_var  = top_bar_1
    top_bar_2_var  = None

screens = [
    Screen(top=top_bar_1_var, bottom=bar.Gap(bar_gap_size), left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size)),
    Screen(top=top_bar_2_var, bottom=bar.Gap(bar_gap_size), left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size)) 
    ]
        
### HOOKS ###
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

wmname = "LG3D"