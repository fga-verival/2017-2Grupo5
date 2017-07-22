# The last version of vagrant configuration
Vagrant.configure("2") do |config|

  # Configure the image of virtualbox
  config.vm.box = "ubuntu-server-14.04"
  config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"

  # Create machine call tbl
  config.vm.define :tbl do |web_config|

    # Create a private network with ip defined
    web_config.vm.network "private_network", ip: "192.168.50.10"

    # Mapping ports to localhost 8080
    config.vm.network :forwarded_port, host_ip: "127.0.0.1", guest: 8080, host: 8080

    # Provision to install the enviroment dependency
    config.vm.provision "shell", inline: <<-SHELL
      # Update and upgrade the server packages
      sudo apt-get update
      sudo apt-get -y upgrade

      # Set Ubuntu Language
      sudo locale-gen en_GB.UTF-8

      # Install Python, SQLite and pip
      sudo apt-get install -y python3-dev sqlite python3-pip

      # Upgrade pip to the lastest version
      sudo pip3 install --upgrade pip

      # Install and configure python virtualenvwrapper.
      sudo pip3 install virtualenvwrapper
      if ! grep -q VIRTUALENV_ALREADY_ADDED /home/vagrant/.bashrc; then
        echo "# VIRTUALENV_ALREADY_ADDED" >> /home/vagrant/.bashrc
        echo "WORKON_HOME=~/.virtualenvs" >> /home/vagrant/.bashrc
        echo "PROJECT_HOME=/vagrant" >> /home/vagrant/.bashrc
        echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
      fi
    SHELL
  end
end
