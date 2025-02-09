# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)

"""Banner module to display the depthviz banner.

This module contains the banner to display the depthviz banner in the command line interface.

Constants:
    DEFAULT: The default color style.
    BRIGHT: The bright cyan color style.
    MID: The mid cyan color style.
    DARK: The dark cyan color style.
    RESET: Reset all colors + styles.
    BANNER: The depthviz banner.
"""

from colorama import Fore, Style, init

# Color styles
DEFAULT = Style.BRIGHT
BRIGHT = Fore.CYAN + Style.BRIGHT
MID = Fore.CYAN + Style.NORMAL
DARK = Fore.CYAN + Style.DIM
RESET = Fore.RESET + Style.RESET_ALL

# depthviz banner
BANNER = f"""
{BRIGHT}sss{RESET}  {MID}++++++++++{RESET}  {DARK}mmmmmmmm{RESET}                                                    
 {BRIGHT}sss{RESET}  {DARK}mmm{RESET}  {MID}+++{RESET}  {DARK}mmm{RESET}  {BRIGHT}sss{RESET}                                                     
  {BRIGHT}sss{RESET}  {DARK}mmm{RESET}  {MID}+{RESET}  {DARK}mmm{RESET}  {BRIGHT}sss{RESET}     {DEFAULT}_                  _     _{RESET}             {BRIGHT}_ (){RESET}      
   {BRIGHT}sss{RESET}  {DARK}mmm{RESET}   {DARK}mmm{RESET}  {BRIGHT}sss{RESET}     {DEFAULT}| |                | |   | |{RESET}           {BRIGHT}(_){RESET}        
    {BRIGHT}sss{RESET}  {DARK}mmm{RESET} {DARK}mmm{RESET}  {BRIGHT}sss{RESET}    {DEFAULT}__| |   ___   _ __   | |_  | |__{RESET}   {BRIGHT}__   __  _   ____{RESET}
     {BRIGHT}sss{RESET}  {DARK}mmmmm{RESET}  {BRIGHT}sss{RESET}    {DEFAULT}/ _` |  / _ \\ | '_ \\  | __| | '_ \\{RESET}  {BRIGHT}\\ \\ / / | | |_  /{RESET}
      {BRIGHT}sss{RESET}  {DARK}mmm{RESET}  {BRIGHT}sss{RESET}    {DEFAULT}| (_| | |  __/ | |_) | | |_  | | | |{RESET}  {BRIGHT}\\ V /  | |  / /{RESET} 
       {BRIGHT}sss{RESET}  {DARK}m{RESET}  {BRIGHT}sss{RESET}      {DEFAULT}\\__,_|  \\___| | .__/   \\__| |_| |_|{RESET}   {BRIGHT}\\_/   |_| /___|{RESET}
        {BRIGHT}sss{RESET}   {BRIGHT}sss{RESET}                     {DEFAULT}| |{RESET}                                    
         {BRIGHT}sssssss{RESET}                      {DEFAULT}|_|{RESET}                                    
           {BRIGHT}sss{RESET}                                                               
            {BRIGHT}s{RESET}                                                                
"""  # noqa: E501


class Banner:
    """Banner class to display the depthviz banner."""

    @staticmethod
    def print_banner() -> None:
        """Prints the depthviz banner."""
        init()
        print(BANNER)
