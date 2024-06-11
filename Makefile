init:
	git clone git@github.com:Superfuds/odoo.git user
	git submodule update --init
	ln -sf odoo-ce/odoo odoo
	pyenv virtualenv 3.8.5 odoo
	eval "$(pyenv virtualenv-init -)"
	cd odoo-ce && pip3 install --upgrade setuptools wheel
	cd odoo-ce && pip3 install -r requirements.txt
	cd user && pip3 install -r requirements.txt
	cd user && git submodule update --init

install_dependencies:
	docker exec odoo_web pip3 install --upgrade pip
	docker exec odoo_web pip3 install -r /mnt/extra-addons/requirements.txt
	docker exec odoo_web pip3 install awscli --ignore-installed six
