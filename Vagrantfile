# -*- mode: ruby -*-
# # vi: set ft=ruby :

require 'fileutils'

Vagrant.require_version ">= 1.6.0"

$num_instances = 3
$update_channel = "stable"
$enable_serial_logging = false
$vb_gui = false
$vb_memory = 700
$vb_cpus = 1
$expose_docker_tcp = 2375
$expose_etcd = 4001


Vagrant.configure("2") do |config|
  config.vm.box = "coreos-%s" % $update_channel
  config.vm.box_version = ">= 308.0.1"
  config.vm.box_url = "http://%s.release.core-os.net/amd64-usr/current/coreos_production_vagrant.json" % $update_channel

  config.vm.provider :vmware_fusion do |vb, override|
    override.vm.box_url = "http://%s.release.core-os.net/amd64-usr/current/coreos_production_vagrant_vmware_fusion.json" % $update_channel
  end

  config.vm.provider :virtualbox do |v|
    # On VirtualBox, we don't have guest additions or a functional vboxsf
    # in CoreOS, so tell Vagrant that so it can be smarter.
    v.check_guest_additions = false
    v.functional_vboxsf     = false
  end

  # plugin conflict
  if Vagrant.has_plugin?("vagrant-vbguest") then
    config.vbguest.auto_update = false
  end


  # replaces token with a new value when doing "vagrant up"
  var_file = 'group_vars/all'
  example_var_file = var_file + '.example'

  if !File.exists?(var_file)
    FileUtils.copy_file(example_var_file, var_file)
  end

  if ARGV[0].eql?('destroy')
    FileUtils.rm(var_file)
  end

  if ARGV[0].eql?('up')
    require 'open-uri'

    cluster_token = open('https://discovery.etcd.io/new').read

    # writes ansible configuration
    text = File.read(var_file)
    new_contents = text.gsub(/<cluster_token>/, 'cluster_token: ' + cluster_token)

    File.open(var_file, "w") {|file| file.puts new_contents }
  end


  (1..$num_instances).each do |i|
    config.vm.define vm_name = "core-%02d" % i do |config|
      config.vm.hostname = vm_name


      if $enable_serial_logging
        logdir = File.join(File.dirname(__FILE__), "log")
        FileUtils.mkdir_p(logdir)

        serialFile = File.join(logdir, "%s-serial.txt" % vm_name)
        FileUtils.touch(serialFile)

        config.vm.provider :vmware_fusion do |v, override|
          v.vmx["serial0.present"] = "TRUE"
          v.vmx["serial0.fileType"] = "file"
          v.vmx["serial0.fileName"] = serialFile
          v.vmx["serial0.tryNoRxLoss"] = "FALSE"
        end

        config.vm.provider :virtualbox do |vb, override|
          vb.customize ["modifyvm", :id, "--uart1", "0x3F8", "4"]
          vb.customize ["modifyvm", :id, "--uartmode1", serialFile]
        end
      end

      if $expose_etcd
        config.vm.network "forwarded_port", guest: 4001, host: ($expose_etcd + i - 1), auto_correct: true
      end

      if $expose_docker_tcp
        config.vm.network "forwarded_port", guest: 2375, host: ($expose_docker_tcp + i - 1), auto_correct: true
      end

      config.vm.provider :vmware_fusion do |vb|
        vb.gui = $vb_gui
      end

      config.vm.provider :virtualbox do |vb|
        vb.gui = $vb_gui
        vb.memory = $vb_memory
        vb.cpus = $vb_cpus
      end

      config.vm.provision "ansible" do |ansible|
        ansible.playbook = "bootstrap.yml"
        # we do not provide any inventory, vagrant will generate one for us
        # see https://docs.vagrantup.com/v2/provisioning/ansible.html

        core_list = (1..$num_instances).to_a.map {|index| "core-0#{index}"}

        ansible.groups = {
          "coreos" => core_list,
          "all_groups:children" => ["coreos"]
        }

        ansible.limit = 'all'
        ansible.verbose = 'vvvv'
        ansible.host_key_checking = false
      end

      ip = "172.12.8.#{i+100}"
      config.vm.network :private_network, ip: ip

      # Uncomment below to enable NFS for sharing the host machine into the coreos-vagrant VM.
      config.vm.synced_folder ".", "/home/core/share", id: "core", :nfs => true, :mount_options => ['nolock,vers=3,udp']

    end
  end
end
