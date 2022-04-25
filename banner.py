class colors:
    blue='\033[34m'
    purple='\033[35m'
    white= '\033[37m'

def banner():
  banner = f"""
{colors.purple}_____________    {colors.white} ___   ___                      _
{colors.purple}(      {colors.blue}|%%|{colors.purple} )--  {colors.white}|     |   |     /   /|  /| | / |
{colors.purple} (     {colors.blue}|%%|{colors.purple})   | {colors.white}|---  |   |    / | / | /-| |\  |-
{colors.purple}  (       )----  {colors.white}|___| |___|   /  |/  |/  | | \ |_
{colors.purple}   (_____)       {colors.white}
              ___                 _    ____  _
             |       /|   /|  /| |       |  |    /|
             |---|  /-|  / | / | |-      |  |-  /-|
              ___| /  | /  |/  | |_      |  |_ /  |
"""
  print(banner)

if __name__=='__main__':
  banner()