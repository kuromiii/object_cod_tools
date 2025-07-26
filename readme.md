# object_cod_tools

## Introduction

object_cod_tools is a Blender addon to assist in the editing of Call of Duty(R) viewmodel assets, though this may be expanded further later.  By default, when importing a CoD asset into Blender, animations will refuse to apply correctly.  This tool fixes that, including:
* Bone renaming
* Weapon assembly from separate armatures and pieces
* Weapon binding, which attaches the weapon bone to the hand and correctly positions it

For users simply hoping to import Call of Duty(R) assets, this eliminates the need for expensive paid software, instead allowing the user to work in Blender, which is free and light on performance.
## Installation

1. Download this repository as a zip
2. Install and open Blender, preferably 2.79 or later.
2. Go to User Preferences, and then Addons.
3. Using the "install from file" dialogue, pick the zip you downloaded.
4. Make sure the checkbox to enable it is checked
5. Save user preferences

## Tutorial

1. Rip the components:
    * the weapon (and potentially parts)
    * the arms
    * Note: FBX and SMD are the most effective formats in my personal experience
2. Position the pieces as you want using Pose Mode.
3. Run CoD Tools - EZ Fix using the spacebar menu
    * MW2 and possibly other games may require you to uncheck the "rename bones" checkbox

## Legal Status
This addon is not endorsed by Call of Duty(R), does not facilitate the breaking of copy protection nor piracy, and does not distribute any assets from the game.  With this in mind, I believe the addon fits under U.S. fair use policy.  However, I may be contacted at my Git email if there are any complaints.