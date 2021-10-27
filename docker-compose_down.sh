#!/bin/bash
sudo docker exec is2_project_db_1 pg_dump -Fc -U root is_prod > db.dump
sudo docker-compose down