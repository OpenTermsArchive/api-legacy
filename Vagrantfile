# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define "ota" do |ota|
    ota.vm.box = "debian/buster64"
    ota.vm.network :forwarded_port, guest: 22, host: 2223, id: 'ssh'
    ota.vm.network "private_network", ip: "192.168.33.11"
    ota.ssh.port = "2223"
    ota.vm.define "ota"
    ota.vm.hostname = "ota"
  end
end
