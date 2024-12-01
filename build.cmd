pyinstaller main.py --onefile ^
                    --distpath ../ ^
                    --specpath ./build_cache ^
                    --workpath ./build_cache ^
                    --name=bot

pyinstaller _print_orders.py --onefile ^
                             --distpath ../ ^
                             --specpath ./build_cache ^
                             --workpath ./build_cache ^
                             --name=print_orders

pyinstaller _reset_db.py --onefile ^
                         --distpath ../ ^
                         --specpath ./build_cache ^
                         --workpath ./build_cache ^
                         --name=reset_db
