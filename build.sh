#!/bin/bash

# Ititialization

mainmenu () {
    des_db_name=test_db
    prod_db_name=is_prod
    db_user=root

    username="Wwwolfgang"
    password="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"

    red=`tput setaf 1`
    green=`tput setaf 2`
    reset=`tput sgr0`
    repo=is2_project
    echo -e "${red}<<< Bienvenidos al Projecto de IS2 del equipo 15 >>>${reset}"

    git clone "https://${username}:${password}@github.com/Wwwolfgang/is2_project.git"

    cd "is2_project"

    echo -e "${green}\n>>> Repository clonado${reset}"
    echo "Presione 1 para Desarrollo"
    echo "Presione 2 para Producción"
    echo "Presione 3 para salir"

    read -n 1 -p "Seleccione:" mainmenuinput
    if [ "$mainmenuinput" = "1" ]
    then
        clear
        echo -e "${green}\n>>> Desarrollo${reset}"
        git checkout main
        git branch
        git pull origin main
        echo "Presione 1 para TAG v.0.0.1"
        echo "Presione 2 para TAG v.0.0.2"
        echo "Presione 3 para TAG v.0.0.3"
        echo "Presione 4 para TAG v.0.0.4"
        echo "Presione 5 para TAG v.0.0.5"
        read -n 1 -p "Seleccione el Tag:" tag

        echo -e "${green}\n>>> Desarrollo TAG v.0.0.${tag}:${reset}"
        echo
         # prepare docker and database
        echo -e "${green}\n>>> Iniciando docker${reset}"
        . docker-compose_up.sh
        sleep 2
        echo
        sudo docker cp db.dump pg_container:/
        echo -e "${green}\n>>> Copiando backup a la BD${reset}"
        sudo docker exec -it pg_container dropdb -U ${db_user} --if-exists ${des_db_name}
        sudo docker exec -it pg_container createdb -U ${db_user} ${des_db_name}
        sudo docker exec -it pg_container psql -U ${db_user} -d ${des_db_name} -c "DROP SCHEMA public CASCADE;"
        sudo docker exec -it pg_container psql -U ${db_user} -d ${des_db_name} -c "CREATE SCHEMA public;"
        sudo docker exec -it pg_container pg_restore -U ${db_user} -d ${des_db_name} --no-owner db.dump
        echo

        if [ "$tag" = "1" ]; then
            git switch --detach v.0.0.1
        elif [ "$tag" = "2" ]; then
            git switch --detach v.0.0.2
        elif [ "$tag" = "3" ]; then
            git switch --detach v.0.0.3
        elif [ "$tag" = "4" ]; then
            git switch --detach v.0.0.4
        elif [ "$tag" = "5" ]; then
            git switch --detach v.0.0.5
        else 
            echo -e "${red}\n<<< Esa versión no existe >>>${reset}"
            sleep 2
            exit
        fi

         # prepare env and install dependencies
        echo -e "${green}\n>>> Creando entorno virtual${reset}"
        python3 -m venv env
        echo "${green}>>> env fue creado${reset}"
        sleep 2
        echo "${green}>>> Activando el env${reset}"
        source env/bin/activate
        sleep 2
        echo "${green}>>> Instalando dependencias${reset}"
        pip install -r requirements.txt

        echo -e "${green}\n>>> Listo para trabajar${reset}"
        echo
        python manage.py runserver

    elif [ "$mainmenuinput" = "2" ]; then
        clear
        echo -e "${green}\n>>> Producción${reset}"
        git checkout production
        git branch
        git pull origin production
        echo "Presione 1 para TAG v.0.0.1"
        echo "Presione 2 para TAG v.0.0.2"
        echo "Presione 3 para TAG v.0.0.3"
        echo "Presione 4 para TAG v.0.0.4"
        echo "Presione 5 para TAG v.0.0.5"
        read -n 1 -p "Seleccione el Tag:" tag
        echo -e "${green}\n>>> Producción TAG v.0.0.${tag}:${reset}"
        echo
        

        if [ "$tag" = "1" ];
        then
            git switch --detach vp.0.0.1
            git checkout production db.dump
        elif [ "$tag" = "2" ]; then
            git switch --detach vp.0.0.2
            git checkout production db.dump
        elif [ "$tag" = "3" ]; then
            git switch --detach vp.0.0.3
            git checkout production db.dump
        elif [ "$tag" = "4" ]; then
            git switch --detach vp.0.0.4
            git checkout production db.dump
        elif [ "$tag" = "5" ]; then
            git switch --detach vp.0.0.5
            git checkout production db.dump
        else 
            echo -e "${red}\n<<< Esa versión no existe >>>${reset}"
            sleep 2
            exit
        fi

        . docker-compose_up.sh
        sleep 2
        echo

        sudo docker cp db.dump is2_project_db_1:/
        echo -e "${green}\n>>> Copiando backup a la BD${reset}"
        sudo docker exec -it is2_project_db_1 dropdb -U ${db_user} --if-exists ${prod_db_name}
        sudo docker exec -it is2_project_db_1 createdb -U ${db_user} ${prod_db_name}
        sudo docker exec -it is2_project_db_1 psql -U ${db_user} -d ${prod_db_name} -c "DROP SCHEMA public CASCADE;"
        sudo docker exec -it is2_project_db_1 psql -U ${db_user} -d ${prod_db_name} -c "CREATE SCHEMA public;"
        sudo docker exec -it is2_project_db_1 pg_restore -U ${db_user} -d ${prod_db_name} --no-owner db.dump

        sleep 2
        echo -e "${green}\n>>> Juntar static files${reset}"
        sudo docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear

        echo
        echo -e "${green}\n>>> Listo para trabajar${reset}"

    elif [ "$mainmenuinput" = "3" ]; then
        echo -e "${red}\n<<< Finalizar >>>${reset}"
        sleep 2
        clear
    else
        echo -e "\nOpción invalida"
        echo -e "\nPrueba de nuevo!!"
        echo ""
        echo "Presione una tecla"
        read -n 1
        clear
        mainmenu
    fi
    cd ..
}

# This builds the main menu and routs the user to the function selected.

mainmenu