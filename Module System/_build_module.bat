@echo off
python -tt _build_module.pyw -d
@del *.pyc
echo
echo Press any key to exit...
pause>nul
