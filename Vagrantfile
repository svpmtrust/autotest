# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "hashicorp/precise64"
  local_ip = "10.0.2.2"
  contest_name = "GnanaTechContest"


  config.vm.define "gitserver" do |gitserver|
    gitserver.vm.provision :shell, path: "gitserver/bootstrap.sh" ,args: ["/vagrant", local_ip, contest_name]
    gitserver.vm.network :forwarded_port, guest: 80, host: 12003, protocol: 'tcp'
    gitserver.vm.network "private_network", ip: "192.168.50.1"
  end

  config.vm.define "testserver" do |testserver|
    testserver.vm.provision "shell", path: "testserver/provision.sh" ,args: ["/vagrant", local_ip, contest_name, "192.168.50.1"]
    testserver.vm.network "private_network", ip: "192.168.50.2"
  end
  
  config.vm.define "testcoordinator" do |testcoordinator|
    testcoordinator.vm.provision "shell", path: "testcoordinator/provision.sh" ,args: ["/vagrant", local_ip, contest_name, "192.168.50.1"]
    testcoordinator.vm.network "private_network", ip: "192.168.50.3"
  end


end
