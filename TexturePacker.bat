@ECHO OFF

COLOR A

ECHO -------------------------------------------------------------------------
ECHO ^> ** Creating excludes... **

ECHO .svn>exclude.txt
ECHO .git>>exclude.txt
ECHO Thumbs.db>>exclude.txt
ECHO Desktop.ini>>exclude.txt
ECHO dsstdfx.bin>>exclude.txt
ECHO build.bat>>exclude.txt
ECHO C:\Users\kevng\AppData\Roaming\Kodi\addons\skin.touchy\media\>>exclude.txt
ECHO C:\Users\kevng\AppData\Roaming\Kodi\addons\skin.touchy\backgrounds\>>exclude.txt
ECHO exclude.txt>>exclude.txt

ECHO -------------------------------------------------------------------------
ECHO.

ECHO -------------------------------------------------------------------------
ECHO                   ** Creating Textures XBT File... **
ECHO -------------------------------------------------------------------------

ECHO.
PING -n 2 -w 1000 127.0.0.1 > NUL
START /B /WAIT TexturePacker -dupecheck -input media\ -output media\Textures.xbt
PING -n 2 -w 20000 127.0.0.1 > NUL
ECHO.
ECHO.
ECHO -------------------------------------------------------------------------
ECHO ^> Deleting excludes...
DEL exclude.txt
ECHO ^> Done
ECHO -------------------------------------------------------------------------
ECHO.
ECHO.
ECHO ----------------------------------------
Echo Copying other files
ECHO ----------------------------------------

for /f "tokens=*" %%c in ('dir /b/ad %1') do xcopy "%1\%%c" "BUILD\%1\%%c" /Q /S /I /Y /EXCLUDE:exclude.txt
for /f "tokens=*" %%c in ('dir /b/a-d %1') do copy %1\%%c "BUILD\%1\%%c"

del exclude.txt

FOR /F "skip=2 Tokens=2 Delims== " %%V IN ('FIND "    version=" "BUILD\%1\addon.xml"') DO SET Version=%%~V

ECHO ----------------------------------------
ECHO Current skin version is %Version%
ECHO ----------------------------------------

cd BUILD
 TexturePacker\zip -r -q %1-%Version%.zip %1

ECHO ----------------------------------------
ECHO Moving files to repository
ECHO ----------------------------------------

if exist "C:\Users\kevng\AppData\Roaming\Kodi\addons\rebuilt.addons\%1\" rmdir "\rebuilt.addons\%1\" /S /Q
md "\rebuilt.addons\%1\"
copy "%1-%Version%.zip" "\rebuilt.addons\%1\"
copy "%1\fanart.jpg" "\rebuilt.addons\%1\fanart.jpg"
copy "%1\icon.png" "\rebuilt.addons\%1\icon.png"
copy "%1\icon.gif" "\rebuilt.addons\%1\icon.gif"
copy "%1\addon.xml" "\rebuilt.addons\%1\addon.xml"
copy "%1\changelog.txt" "\rebuilt.addons\%1\changelog-%Version%.txt"

ECHO ----------------------------------------
ECHO Removing BUILD folder
ECHO ----------------------------------------

cd ..
rmdir BUILD /S /Q

ECHO ----------------------------------------
ECHO Generating addons.xml and addons.xml.md5
ECHO ----------------------------------------

F:
cd C:\Users\kevng\AppData\Roaming\Kodi\addons\rebuilt.addons\
python C:\SkinBuilder\addons_xml_generator.py

ECHO -------------------------------------------------------------------------
ECHO        ** XBT build complete - scroll up to check for errors. **
ECHO -------------------------------------------------------------------------

PING -n 50 -w 5000 127.0.0.1 > NUL