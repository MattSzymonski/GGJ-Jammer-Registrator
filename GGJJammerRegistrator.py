
# GGJ Jammer Registrator
# Copyright (c) 2020 Mateusz Szymonski
# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

import traceback
import time
import sys
import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import tkinter.scrolledtext as scrolledtext

icon = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAsTAAALEwEAmpwYAAAKT2lDQ1BQaG90b3Nob3AgSUNDIHByb2ZpbGUAAHjanVNnVFPpFj333vRCS4iAlEtvUhUIIFJCi4AUkSYqIQkQSoghodkVUcERRUUEG8igiAOOjoCMFVEsDIoK2AfkIaKOg6OIisr74Xuja9a89+bN/rXXPues852zzwfACAyWSDNRNYAMqUIeEeCDx8TG4eQuQIEKJHAAEAizZCFz/SMBAPh+PDwrIsAHvgABeNMLCADATZvAMByH/w/qQplcAYCEAcB0kThLCIAUAEB6jkKmAEBGAYCdmCZTAKAEAGDLY2LjAFAtAGAnf+bTAICd+Jl7AQBblCEVAaCRACATZYhEAGg7AKzPVopFAFgwABRmS8Q5ANgtADBJV2ZIALC3AMDOEAuyAAgMADBRiIUpAAR7AGDIIyN4AISZABRG8lc88SuuEOcqAAB4mbI8uSQ5RYFbCC1xB1dXLh4ozkkXKxQ2YQJhmkAuwnmZGTKBNA/g88wAAKCRFRHgg/P9eM4Ors7ONo62Dl8t6r8G/yJiYuP+5c+rcEAAAOF0ftH+LC+zGoA7BoBt/qIl7gRoXgugdfeLZrIPQLUAoOnaV/Nw+H48PEWhkLnZ2eXk5NhKxEJbYcpXff5nwl/AV/1s+X48/Pf14L7iJIEyXYFHBPjgwsz0TKUcz5IJhGLc5o9H/LcL//wd0yLESWK5WCoU41EScY5EmozzMqUiiUKSKcUl0v9k4t8s+wM+3zUAsGo+AXuRLahdYwP2SycQWHTA4vcAAPK7b8HUKAgDgGiD4c93/+8//UegJQCAZkmScQAAXkQkLlTKsz/HCAAARKCBKrBBG/TBGCzABhzBBdzBC/xgNoRCJMTCQhBCCmSAHHJgKayCQiiGzbAdKmAv1EAdNMBRaIaTcA4uwlW4Dj1wD/phCJ7BKLyBCQRByAgTYSHaiAFiilgjjggXmYX4IcFIBBKLJCDJiBRRIkuRNUgxUopUIFVIHfI9cgI5h1xGupE7yAAygvyGvEcxlIGyUT3UDLVDuag3GoRGogvQZHQxmo8WoJvQcrQaPYw2oefQq2gP2o8+Q8cwwOgYBzPEbDAuxsNCsTgsCZNjy7EirAyrxhqwVqwDu4n1Y8+xdwQSgUXACTYEd0IgYR5BSFhMWE7YSKggHCQ0EdoJNwkDhFHCJyKTqEu0JroR+cQYYjIxh1hILCPWEo8TLxB7iEPENyQSiUMyJ7mQAkmxpFTSEtJG0m5SI+ksqZs0SBojk8naZGuyBzmULCAryIXkneTD5DPkG+Qh8lsKnWJAcaT4U+IoUspqShnlEOU05QZlmDJBVaOaUt2ooVQRNY9aQq2htlKvUYeoEzR1mjnNgxZJS6WtopXTGmgXaPdpr+h0uhHdlR5Ol9BX0svpR+iX6AP0dwwNhhWDx4hnKBmbGAcYZxl3GK+YTKYZ04sZx1QwNzHrmOeZD5lvVVgqtip8FZHKCpVKlSaVGyovVKmqpqreqgtV81XLVI+pXlN9rkZVM1PjqQnUlqtVqp1Q61MbU2epO6iHqmeob1Q/pH5Z/YkGWcNMw09DpFGgsV/jvMYgC2MZs3gsIWsNq4Z1gTXEJrHN2Xx2KruY/R27iz2qqaE5QzNKM1ezUvOUZj8H45hx+Jx0TgnnKKeX836K3hTvKeIpG6Y0TLkxZVxrqpaXllirSKtRq0frvTau7aedpr1Fu1n7gQ5Bx0onXCdHZ4/OBZ3nU9lT3acKpxZNPTr1ri6qa6UbobtEd79up+6Ynr5egJ5Mb6feeb3n+hx9L/1U/W36p/VHDFgGswwkBtsMzhg8xTVxbzwdL8fb8VFDXcNAQ6VhlWGX4YSRudE8o9VGjUYPjGnGXOMk423GbcajJgYmISZLTepN7ppSTbmmKaY7TDtMx83MzaLN1pk1mz0x1zLnm+eb15vft2BaeFostqi2uGVJsuRaplnutrxuhVo5WaVYVVpds0atna0l1rutu6cRp7lOk06rntZnw7Dxtsm2qbcZsOXYBtuutm22fWFnYhdnt8Wuw+6TvZN9un2N/T0HDYfZDqsdWh1+c7RyFDpWOt6azpzuP33F9JbpL2dYzxDP2DPjthPLKcRpnVOb00dnF2e5c4PziIuJS4LLLpc+Lpsbxt3IveRKdPVxXeF60vWdm7Obwu2o26/uNu5p7ofcn8w0nymeWTNz0MPIQ+BR5dE/C5+VMGvfrH5PQ0+BZ7XnIy9jL5FXrdewt6V3qvdh7xc+9j5yn+M+4zw33jLeWV/MN8C3yLfLT8Nvnl+F30N/I/9k/3r/0QCngCUBZwOJgUGBWwL7+Hp8Ib+OPzrbZfay2e1BjKC5QRVBj4KtguXBrSFoyOyQrSH355jOkc5pDoVQfujW0Adh5mGLw34MJ4WHhVeGP45wiFga0TGXNXfR3ENz30T6RJZE3ptnMU85ry1KNSo+qi5qPNo3ujS6P8YuZlnM1VidWElsSxw5LiquNm5svt/87fOH4p3iC+N7F5gvyF1weaHOwvSFpxapLhIsOpZATIhOOJTwQRAqqBaMJfITdyWOCnnCHcJnIi/RNtGI2ENcKh5O8kgqTXqS7JG8NXkkxTOlLOW5hCepkLxMDUzdmzqeFpp2IG0yPTq9MYOSkZBxQqohTZO2Z+pn5mZ2y6xlhbL+xW6Lty8elQfJa7OQrAVZLQq2QqboVFoo1yoHsmdlV2a/zYnKOZarnivN7cyzytuQN5zvn//tEsIS4ZK2pYZLVy0dWOa9rGo5sjxxedsK4xUFK4ZWBqw8uIq2Km3VT6vtV5eufr0mek1rgV7ByoLBtQFr6wtVCuWFfevc1+1dT1gvWd+1YfqGnRs+FYmKrhTbF5cVf9go3HjlG4dvyr+Z3JS0qavEuWTPZtJm6ebeLZ5bDpaql+aXDm4N2dq0Dd9WtO319kXbL5fNKNu7g7ZDuaO/PLi8ZafJzs07P1SkVPRU+lQ27tLdtWHX+G7R7ht7vPY07NXbW7z3/T7JvttVAVVN1WbVZftJ+7P3P66Jqun4lvttXa1ObXHtxwPSA/0HIw6217nU1R3SPVRSj9Yr60cOxx++/p3vdy0NNg1VjZzG4iNwRHnk6fcJ3/ceDTradox7rOEH0x92HWcdL2pCmvKaRptTmvtbYlu6T8w+0dbq3nr8R9sfD5w0PFl5SvNUyWna6YLTk2fyz4ydlZ19fi753GDborZ752PO32oPb++6EHTh0kX/i+c7vDvOXPK4dPKy2+UTV7hXmq86X23qdOo8/pPTT8e7nLuarrlca7nuer21e2b36RueN87d9L158Rb/1tWeOT3dvfN6b/fF9/XfFt1+cif9zsu72Xcn7q28T7xf9EDtQdlD3YfVP1v+3Njv3H9qwHeg89HcR/cGhYPP/pH1jw9DBY+Zj8uGDYbrnjg+OTniP3L96fynQ89kzyaeF/6i/suuFxYvfvjV69fO0ZjRoZfyl5O/bXyl/erA6xmv28bCxh6+yXgzMV70VvvtwXfcdx3vo98PT+R8IH8o/2j5sfVT0Kf7kxmTk/8EA5jz/GMzLdsAAAAgY0hSTQAAeiUAAICDAAD5/wAAgOkAAHUwAADqYAAAOpgAABdvkl/FRgAAEDNJREFUeNrcW3dUVNf2/qYXGIqCigUUFWvK08TEJ0Z/JmJJYokFG4o1b1SkiBo10YhGMfFpYlSMjdgFnyXWmJc8E6PGKNiQgChSBBUsyDAMzACzf39wZ7hzuTPcUfGt9fZad61bTvu+c84+++yzr4iIAAAikQgvQTwB9AbQHEA5gEsAruK/JEQE6UusTwZgAoD3ATQCYATwFoANAC7jv8mCZRTUo4QAqABAdq7DwEvtDCv2l0HA1w6As6+7ALz/1wgI5wGaBuB7AEcA6DjfbgMQ/68Q4AOgigNwGieNHMABTpotL6j+dwD0qXcCjAZP3gvAIg6wiQ7SxnPSvmovLU9ePtnQM1BKvXtLiVGydgmol+GmUBe1BTCQ9eqq0eAZ74DEiQByWa9mP0f1G4YMlml//kmDUyc0GDlCrnVEQn3NtzcAvMZ6Pi0gzyLW/TiFuqjBs4JP2OtqfbFzuwsGfSizS0J9EeALQMl6vi0gTwKAYla7Bj4veIvsT3DFsI/4R0J9EWDkzgoBuqQcwCHWqw8E1qUBsGHoEDkveIvs2eWCoUNqk1BfBKQCuM967iAw3x+s+84C88TMjlJq9+1xqTPhvj0uGDxIpgUwtL4JuMwxb4ME5vuLdd9coS6SOFC07RTqoisAIhp5C9/HeDUUA4CX5blezE+jwfOxQl10iLH7AcCvZRvV9K7bk29ppOIOzV2krRUStJCKRAqjmaAzmR/eLa3MClj6my7js1GWYtwZy/ABD/gpADa3bStBdnYV5s0vQ0EhYcUXKoftWrykDFvjjXEANr+wvYCD9VkFoNzV1YWWLl1yL//+/VKqQ+4XG2ysxqFr/zWAp9woADQ+RE5Ggyct+lRlSf9wdpSSjAZP3mveXKXFJmjwUgwhIopITU0tLCkpIaGi1+ttCAj8IYf8EnJ2+yXkdGTADwBAE8bLbcBN1yos4DbMia5NwpxoJQFIYazTF2IJKgC48hGg3HM/cMb5h2k3i01kqDALBv+ovIp+unHHCl6tVlOnxEzyS8ghv4QcapmQEwugeFKogreHIyOsPbxh3twaEhbMV1rKLAAwnEuASKBDpDOAIQACAbRhHBtyZjOTB+CcxMP7qN/ujNdEPh5rMlPygfIyvOmjwuF3G6OpulrVJD0y4uLDcjwoq0JMlwa4X1aFw9l6NHeVIfrPx9DcS0NyeD8AQNOAjpAtPVnd0AoTinbEYLRvIr5dq7bbyDnzyrD22/I4APgyVqWVSkWIijbYqAEAMc44RPoA+ARAXzvfXQE0BdCt6unDyPvh76DpiJnYHT4NXRsDIl0FPORibEzXYf1fOqQXm1BZaMScPo2qraWEHFQ+rYDUQwYXqRh+JXnWgj1atkMpC3xoQCJWfal22NivVqoAQLv22/L1JhNgMBCfR8pGHBGwGcAUZ+ZF2e0UZK/4GL9c3Y1B6+Pg2qojEnPKMe/SE5RWmlFVSYCXHE+MZkz6/SFmd/LAtSITzhWUwUMuRtHVs9ayGr/6NjKrKgWDt8gn85Ro7S+eMWWyAlIpkJ9vxuatVrtMJ8QjJAZwnmcfnw5gBYARAN4E8Ka81auBw8Kjbwa+8Tqvk+O77zZa53iRsYr2ZpZQy8Qcwuo02pyuo9IKM7Xdn0sNdmXRK4m3SaWyzlcK2nKaNEEhNGO6wq5m57vmzlESgHUL5tfogckTFQTABCBUiBI8xwFSybOPBwAUmqk9EemJiH788SR17969FgmfzI22UXY3n5rIc0cWdf0hjzx3ZVHDXVnUOjGXBuw4Z80jlUjIO2gMaf/hHHjWUucFYENUZC0SYusigLuHfwQgwM5e2oWIKrnafPXqVbVImDZ1qk2aib8XEuIyqMmebGqVWK3lW82MtaZXtupE7MYLuSLCreAt83wwALpw3o2MBk9Kve5OADIcEeDOM4wDHDgT9thb0s6cOUOuri42ZU2ZMtn6PeqPQsKmW9Ylzi8hh2QBr1jTOjJo6gBvURSdABjYJE6drCAAkY4ImMEBv9QB+NZ1reu5uTnUrFlTGxJmR4QREVHIuSLClhoCfLdctqYJn+Uc+OjZSpJ3eS+NBb41gIJlMSprmnFj5byeIS4B/+IQ0MABAesFGTePHtUiYcFXX1Of20Reu7KsBHi+P54AUGSEc+AjI5TUeehE8tl2gzx3ZjUA0B5A4coVNeAnhSrsusW4BCSzGprsALyYiHRCLbz8/DxSqVQ2JDSJPULtkoh8d2eS75bkZxr2s8KUpNVqSa/X08FsPbWfEbsXgJHd8+ND5HX6BNkE/MZq5FYHmfqTk3LlymWSswgQSyXkv+8m+f9iJPVrgTR3jnPgtf9Q0Eeh0yitUEcPHjyg0NAJBIDY4EePcgyej4A4FgGnHGT6hp5BTp46YTMKFI2ak/uHU2nmDOeWuqhIJfUYOYm6rP+FRodOtpa3fFkN+DGj6wbPR8BUVgPL7GX6d77hrLPgi01mGnaXyGXCUhsSnO35GdMV1KpDZ3LRaGzKWb1KbU0zdoww8HwENOAowam1cvwzVRZ98fFTZ8CnPTWR774cwtZcan+dyO3tfgSAomc7B37mDAWvtRnzeU3PTxgvHLw9Q4h9QFHBcW3D+6cKH59dmfTUWCUI/JHMx9Q4Pp3E6y5Tq3WnqdnKo+T6Vj/6bKHKKfDTpvCDX/VlTc+PHCGnXr16/fG8R2MePGbwSMvHdhfIFfH3aFHSo1pgDYZSSk1NpQMHDlBUZCT5tgkghaJ2w5218MJnVe8PRAA17/4uBU+PpMGDPqSvVqpswGu1WjIYDItfxNngQB62LwAIdesf2sfjlMkYcCCfDBVm0uv1dPz4cRo8eBBJJJI6T4A/mecc+EmhCure/wM6dOUW5ZdWUGZmJmm1WvpmjdpG4Wm1WiIiWrJkyUMA15j9zA4AYQBaPsvZYCgfADFAPrtvVzQ5UEifRYaRSMCxtwggmUpN7N2ZkGv4sBpgFtFqtRS7vKbng0fapgkLC7PXjr0Amjh7OPouc5RdQ4BETN6L95LUxZW3IqVSQb7detMbHy+goHVHqMe6U9Q0KJj4/HTOgt+yZQtNZLnDuOCJiIYOHeKoM0oYTE77BCczBxa8BctkMoqIiKDzF5MoYE8GKeIzyT8xh1psSyFNUAix/XNCrlHBckLXAbSDo2ePHz9O/fvJKOeOOw0cIKsFnojo/fcHHgawGsBBAJl22tzjWZ2iSVzgO3fuIJPJREREC5MeE9ZnUOv9udT8uyTSBIU4vc4z1hsBIpKtu0QXOQBjYmLIx8eHYmJieFcdnjb3R3UgFpuAcsZl7xQBNuf3XXv3pdLSUhtvj9fubPLcmUXNN14iTVAILfrUuaXuo6Fy256SuFKTvRnCNx1EuQ7av41DwkoAbkIJGGXT865eP29OL7apeVuGjrDxFvlu/JM0QSG0+DPnwI8cISePkVpqEvGNLQkKbzpwv1goAfF1dGI6q+wCAOOFEnCTlTEJAG7rTP9h1zzlbCFh2c+kCQqhJYtVTg97Td9x5Lc/j9pdJfIaM9uGBH9fX8rLyxNCQPc6CBjPGQVrhRAwhpOpOzN3PmDX/N735wj/N9bGOBGq7TVBIdV+gX1Z1PLgAwpIJmo4cpYNCe7ubnTx4kVH4NMF6LB2HCy7hITIjGHdH7QcX4tEomMA7gBASkoKMg9sxqoBhzArTCnYChszrhSnSoLRYPKy6hciMchYBtPdR/BZ+A3kwyKsaYuLdejWrRvi47fZKy5KQJUqZyNEvAD0Yj3v5Xwfe/PmTcTFxSHyvUSEzVQIBj8iWI+f9Czw1taIITHqkZ5yH12XrkHEp7aW7aRJkxEaOgGPHz9ivz4vEolOCKh2Muf5QV0EdLac/7GWQauIRCJTeHh4ehv/7fh4qnDwoZNKcdo4qjZ4AFKxCPllBCovRVxzYM3Sz7F503c2abZv34FWrVphZWwsDAZDgUgk6iGg2l4AZrKe0wCcBODwbHAUq9cfAmjG7BABoAsAbdwG9ZRJocLBjxpTip8NwbzgRSKgxGRGkdGMPwY1QzevmnKTk5MREjIOaWm2U93Nze2hTqfbBOAss195yim2JYBJAD7jvP8QwLG6DkenAtjE3BcxBJQxo2KNs+BHjy3FubQOUC45YjdNTnEFdvZpjHGt+WN9Fi5cgOXLV9jLXg4gB8ATZhfrzThJufK1xT1elxLUcw4V/Zl7bVSk0inwI0fpcfCQCe3GRthN87C8Cm/7qOyCB4AvvliOjIybCAwMPM1pH5iotHbMStXTDvj53LMBRwQUcJ4DAXQE8PuevSZkZpoFgQ+ZUIofjlTPHJFPa7vpDCYzOnvIHJZlIqBK7rIw+ezZfkwoXjSAXwGUOsj2hHHytucejdWlAxoCyGLC0AAgo0MHSYCbRoQ/L1bGKZUi7dkzGrzSWeJwzh8+bILFygjcdQV3ZfzHDSUVZqglYqQPbwEXae1YBTMhs+3gUbhzNOEvAGOMBk89Ey9kCZVrw4B0txxWM9bfNWZ68PoDHI2AxwB+ZD0HhIcpcOZXDdq0EWvLyymmew8drqdU8WYePlKPk6XBEElqCCKx/eo85GIUllWi1/F8nCsoR4WZLMQV7zx/bbvU09v/ztGE1gDa8hzZlQC4wijtjcy1HcCf9sALDZNbZ7nx9RUjZFz1vP/1P25o0UK8qKICK3r01OHadVsSgkfrcfRYBVRP7+QRanrTVWmrNywjo9JM0FcQ1HIxku8aEHg0H59fLrpRbDLPA+A7vsfrl6n4kaWg9swq9EKkrgiRM8x5gXbuHCWkTGpvLxGSLrrhre66+dnZ5mU9e+k+vZrsDn9/MYJH63H4h+o5X3TpXHNmfroAQO7F08fwt4FyZv56iAEFAaSWikuUEtGTJmrJjVcDNJf+3kj52weNWlxHFWCqdtBzY41f2I8VQmKE3urUUXLhcpJb7TnyhPD233XIzTWbO3eSiP38xDh+ooJrfQ1ijqohdvU42GLrtd0AWhJRQ4lYpKgyg7xVEl1TlaTQ3012o0djRcrgxr46TlygH4BsdiCI0eC5kqUDnkmE7ga/37LJxe6GJi/Xg9zcRFyvSy6YmH/GArO81wFwEfovACs28A3umUUd/wsIJqAuHdD39dckE0LGyfnjYa9UITzCgOrwPqu5PN5o8PQ1GjyvM+/2s7JomKArZ4UdapvKNcufmwUHI+Bg4j7XWr2efMmNAntICUA+gGOMgREMwNtOD8ZyerCXkyOA7cxYL+CPkRcyBYa/01NqAzwzw50GD5IRgOsAtI4iRTmNFAO4xwJhBtBFYN5lHPI6vywCfjl1QmMFPuwjuWVuzxcSKssDpC+Ph3ZeHXnWcdLHC/xn6LkJGDp4kIzy73pYYmtqAXeWAKaxU3hIeMIAHcNEowYD+ApAISfdLSd+mhJMAN8y6ObmJipu7S/GvfuEggLzUtj+z1OLAGdEoS4aC2CXk23VAehkNHjm8ZRXLyPAjbG2mqB+pC3H2eroumAxpF60vKxfZx3JUAYgH/BsAKPrs3JnosXrU5So/suzM+N3KGN2of9GdaBmvRLw/wMAniMSp71SdeUAAAAASUVORK5CYII='
window=Tk()
window.geometry("300x425")
window.iconphoto(False, PhotoImage(data = icon))
window.configure(bg='#585858')
window.title("GGJ Jammer Registrator")
window.resizable(False, False)

siteAddress = StringVar()
jammersListFilename = None
jammersList = []
driver = None
loggedIn = False;
operating = False


def logPrinter(text):
	print(text)
	log.insert(END,text + "\n")
	log.yview_pickplace("end")
	window.update()

def chooseJammersListFile():
	global jammersListFilename
	try:
		jammersListFilename = filedialog.askopenfilename(parent=None, title = "Select csv file with list of jammers", filetypes =[('csv files',"csv")])
		jammersListLabel.config(text="File loaded", fg="green")
		jammersListFilenameLabel.config(text=jammersListFilename)
	except Exception:
		logPrinter("Failed getting csv file!")

def errorClearWindow(text):
	global operating
	global loggedIn
	
	loggedIn = False
	operating = False

	print(text)
	log.insert(END,text + "\n", 'error')
	log.tag_config('error', foreground='red')
	log.yview_pickplace("end")
	window.update()

	driver.quit()

	registerButton.config(state=NORMAL)
	findNotRegisteredButton.config(state=DISABLED)
	siteAddressEntry.config(state=NORMAL)
	jammersChooseFileButton.config(state=NORMAL)
	window.update()

def setup(operation):

	global driver
	global siteAddress
	global jammersListFilename
	global jammersList 

	if(len(siteAddress.get()) == 0 or jammersListFilename == None):
		logPrinter("Not enough data provided!")
		raise("Not enough data provided!")

	registerButton.config(state=DISABLED)
	findNotRegisteredButton.config(state=DISABLED)
	siteAddressEntry.config(state=DISABLED)
	jammersChooseFileButton.config(state=DISABLED)

	siteAddressText = siteAddress.get()

	try:
		jammersList.clear()
		logPrinter("Opening browser")
		try:
			driver = webdriver.Firefox(service_log_path='NUL', executable_path='geckodriver.exe')
		except Exception as e:
			errorClearWindow("Cannot find geckodriver.exe! \nMake sure it is in the same directory as GGJJammerRegisterer")
			print(e)
			print(traceback.format_exc())
			return
		logPrinter("Opening GGJ website")
		driver.get(siteAddress.get())
		WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@id='block-boxes-footer-links']")))
		
		loginButton = driver.find_element_by_xpath("//a[@href='/user']")
		loginButton.click()
		time.sleep(1)

		print("Please log in to game jam organizer account now \nWhen done click button once again")
		log.insert(END,"Please log in to game jam organizer account now \nWhen done click button once again\n", 'actionRequired')
		log.tag_config('actionRequired', foreground='#FF791C')
		log.yview_pickplace("end")
		window.update()

		if(operation == 1):
			registerButton.config(state=NORMAL)
		if(operation == 2):
			findNotRegisteredButton.config(state=NORMAL)

		window.update()
		while (loggedIn is False):
			window.update()

		registerButton.config(state=DISABLED)
		findNotRegisteredButton.config(state=DISABLED)
		window.update()

		WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//a[@class='user-logout']")))
		time.sleep(1)	
	except Exception as e:
		errorClearWindow("Unhandled error during setup!")
		print(e)
		print(traceback.format_exc())
		return
	
	try:
		logPrinter("Collecting names of already registered jammers")

		organizersFound =  driver.find_element_by_xpath("//div[@id='block-views-jam-site-users-site-org-block']").find_elements_by_xpath(".//a[@class='username']")
		for org in organizersFound:
			jammersList.append(org.text.lower())

		seeAllJammersButton = driver.find_element_by_link_text("See all jammers")
		seeAllJammersButton.click()
		time.sleep(5)
		jammersFound = driver.find_elements_by_xpath("//a[@class='username']")
		for jammer in jammersFound:
			jammersList.append(jammer.text.lower())

	except Exception as e: 
		errorClearWindow("Unhandled error while collecting names of already registered jammers!")
		print(e)
		print(traceback.format_exc())
		return

def findNotRegisteredJammers():
	
	global operating
	global loggedIn

	if (operating is True):
		loggedIn = True
		return
	
	operating = True

	logPrinter("Finding not yet registered jammers")

	setup(2)

	logPrinter("Not yet registered jammers:")
	try:
		with open(jammersListFilename, encoding='utf-8') as csvFile:
			csvReader = csv.reader(csvFile, delimiter=',')

			rowCount = 0
			notRegisteredCount = 0
			for row in csvReader:
				if rowCount == 0:
					rowCount += 1
				else:
					rowCount += 1
					if(row[0].lower() not in jammersList):
						notRegisteredCount += 1
						print(f'{row[0]}\n') 
						log.insert(END, f'\n{row[0]}\n')
						log.yview_pickplace("end")
						window.update()
	except Exception:
		errorClearWindow("Unhandled error while finding not yet registered jammers!")
		print(e)
		print(traceback.format_exc())
		return

	logPrinter(f'\nFinding not yet registered jammers finished! \n{notRegisteredCount} jammers not registered')
	driver.quit()

	registerButton.config(state=NORMAL)
	findNotRegisteredButton.config(state=NORMAL)
	siteAddressEntry.config(state=NORMAL)
	jammersChooseFileButton.config(state=NORMAL)
	loggedIn = False
	operating = False

def registerJammers():
	
	global operating
	global loggedIn

	if (operating is True):
		loggedIn = True
		return
	
	operating = True

	logPrinter("Registered jammers")

	setup(1)
	
	try:
		logPrinter("Setup successful! Starting registration")
		driver.execute_script("window.history.go(-1)")
		WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@id='block-views-jam-site-users-site-org-block']")))
		logPrinter("Moving to \"Add a new jammer\" page")
		addNewJammerButton = driver.find_element_by_xpath("//a[@class='jam-site-admin-link']")
		addNewJammerButton.click()
		WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@id='edit-submit']")))
		logPrinter("Starting registration")

		with open(jammersListFilename, encoding='utf-8') as csvFile:
			csvReader = csv.reader(csvFile, delimiter=',')

			alreadyRegisteredJammers = 0;
			newRegisteredJammers = 0;
			faultyRegisteredJammers = 0;

			rowCount = 0
			for row in csvReader:
				if rowCount == 0:
					rowCount += 1
				else:
					rowCount += 1
					print(f'Registering {row[0]}') 
					log.insert(END,f'Registering {row[0]}\n')
					log.yview_pickplace("end")
					window.update()

					if(row[0].lower() in jammersList):
						alreadyRegisteredJammers += 1
						print(f'Already registered! Skipping\n') 
						log.insert(END, f'Already registered! Skipping\n\n')
						log.yview_pickplace("end")
						window.update()
						continue
		
					newJammerUsername = driver.find_element_by_xpath("//input[@id='edit-name']")
					newJammerUsername.clear()
					newJammerUsername.send_keys(row[0])
					time.sleep(1)
					addJammerButton = driver.find_element_by_xpath("//input[@id='edit-submit']")
					addJammerButton.click()
					time.sleep(5)					

					resultSuccess = None
					try:
						resultSuccess = driver.find_element_by_xpath("//*[contains(text(), 'has been added to the group')]")
					except Exception:
						pass

					resultError = None
					try:
						resultError = driver.find_element_by_xpath("//*[contains(text(), 'You have entered an invalid user name.')]")
					except Exception:
						pass

					if(resultSuccess is not None):
						newRegisteredJammers += 1
						print(f'Success!\n') 
						log.insert(END, f'Success!\n\n')
						log.yview_pickplace("end")
						window.update()
					if(resultError is not None):
						faultyRegisteredJammers += 1
						print(f'Failed! Skipping\n') 
						log.insert(END, f'Failed! Skipping\n\n')
						log.yview_pickplace("end")
						window.update()
					if(resultSuccess is None and resultError is None):
						raise Exception('Cannot get adding jammer operation status')

					window.update()

			logPrinter(f'Registering finished! {rowCount - 1} jammers processed \nNew registered: {newRegisteredJammers} \nAlready registered: {alreadyRegisteredJammers} \nRegistration errors: {faultyRegisteredJammers}')
			driver.quit()
	except Exception as e:
		errorClearWindow("Unhandled error while adding jammers!")
		print(e)
		print(traceback.format_exc())
		return

	

	registerButton.config(state=NORMAL)
	findNotRegisteredButton.config(state=NORMAL)
	siteAddressEntry.config(state=NORMAL)
	jammersChooseFileButton.config(state=NORMAL)
	loggedIn = False
	operating = False


siteAddressLabel = Label(window, text="Web address of your jam site", width=30, fg='white', bg='#585858', justify=CENTER)
siteAddressLabel.place(x=45,y=10)
siteAddressEntry = Entry(window, textvar=siteAddress, width=30)
siteAddressEntry.place(x=60,y=35)

jammersLabel = Label(window, text="Jammers to register (.csv)", width=30, fg='white', bg='#585858', justify=CENTER)
jammersLabel.place(x=45,y=60)
jammersListLabel = Label(window, text="No file choosen", width=12, bg='#585858', fg="red")
jammersListLabel.place(x=150,y=87)
jammersChooseFileButton = Button(window, text="Choose file", relief=FLAT, command=chooseJammersListFile);
jammersChooseFileButton.place(x=60, y=85)
jammersListFilenameLabel = Message(window, text="", width=240, fg='white', bg='#585858')
jammersListFilenameLabel.configure(anchor="center")
jammersListFilenameLabel.place(x=25,y=120)

registerButton = Button(window, text="Start registering", relief=FLAT, bg="#FF5555", command=registerJammers);
registerButton.place(x=40, y=195)

findNotRegisteredButton = Button(window, text="Find not registered", relief=FLAT, bg="#FF5555", command=findNotRegisteredJammers);
findNotRegisteredButton.place(x=155, y=195)

logLabel = Label(window, text="Log", width=30, fg='white', bg='#585858', justify=CENTER)
logLabel.place(x=45,y=230)
log = scrolledtext.ScrolledText(window, width=29, height=9, wrap='word')
log.place(x=25, y=255)


window.mainloop()
