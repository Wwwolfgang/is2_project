#!/bin/bash

# Ititialization

mainmenu () {
    des_db_name=test_db
    prod_db_name=is_prod
    db_user=root
    echo "Presione 1 para Desarrollo"
    echo "Presione 2 para Producción"
    read -n 1 -p "Seleccione:" mainmenuinput
    if [ "$mainmenuinput" = "1" ]
    then
        clear
        echo "Presione 1 para TAG v.0.0.1"
        echo "Presione 2 para TAG v.0.0.2"
        echo "Presione 3 para TAG v.0.0.3"
        echo "Presione 4 para TAG v.0.0.4"
        read -n 1 -p "Seleccione el Tag:" tag
        if [ "$tag" = "1" ];
        then
            echo -e "\nDesarrollo TAG v.0.0.1:"
            echo
            # git checkout tags/v.0.0.4 -b v.0.0.4-branch
            . docker-compose_up.sh
            echo
            sudo docker cp db.dump pg_container:/
            echo -e "\nCopiando backup a la BD..."
            sudo docker exec -it pg_container dropdb -U ${db_user} --if-exists ${des_db_name}
            sudo docker exec -it pg_container createdb -U ${db_user} ${des_db_name}
            sudo docker exec -it pg_container psql -U ${db_user} -d ${des_db_name} -c "DROP SCHEMA public CASCADE;"
            sudo docker exec -it pg_container psql -U ${db_user} -d ${des_db_name} -c "CREATE SCHEMA public;"
            sudo docker exec -it pg_container pg_restore -U ${db_user} -d ${des_db_name} --no-owner db.dump
            echo "Listo para trabajar"
        fi

    elif [ "$mainmenuinput" = "2" ]; then
        installsamba
        quitprogram
    else
        echo "You have entered an invallid selection!"
        echo "Please try again!"
        echo ""
        echo "Press any key to continue..."
        read -n 1
        clear
        mainmenu
    fi
}

# This builds the main menu and routs the user to the function selected.

mainmenu

# This executes the main menu function.
# Let the fun begin!!!! WOOT WOOT!!!!