# -*- mode: ruby -*-
# vi: set ft=ruby :
ENV['VAGRANT_NO_PARALLEL'] = 'yes'

domain = "tinystage.test"

machines = {
  "freeipa": {
    "vm.hostname": "ipa.#{domain}",
    "hostmanager.aliases": ["kerberos"],
    "autostart": true,
  },
  "fasjson": {"autostart": true},
  "ipsilon": {"autostart": true},
  "oidctest": {},
  "openidtest": {},
  "fas2ipa": {
    "libvirt.memory": 4096,
  },
  "noggin": {},
  "elections": {},
  "mirrormanager2": {},
  "ipaclient": {},
}

Vagrant.configure(2) do |config|
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true

  machines.each do |mname, mdef|
    autostart = mdef.fetch(:autostart, false)
    mdef.delete(:autostart)
    config.vm.define mname, autostart: autostart do |machine|
      machine.vm.box_url = "https://download.fedoraproject.org/pub/fedora/linux/releases/33/Cloud/x86_64/images/Fedora-Cloud-Base-Vagrant-33-1.2.x86_64.vagrant-libvirt.box"
      machine.vm.box = "f33-cloud-libvirt"
      machine.vm.hostname = "#{mname}.#{domain}"

      libvirt_def = {
        "cpus": 2,
        "memory": 2048,
      }

      mdef.each do |prop, value|
        prop = prop.to_s

        if prop == "hostmanager.aliases"
          value = value.map {|n| "#{n}.#{domain}"}.compact
        end

        prop_elems = prop.split(".")

        if prop_elems[0] == "libvirt"
          dct = libvirt_def
          prop_elems[1..-2].each do |key|
            dct = dct[key]
          end
          dct[prop_elems[-1]] = value
        else
          obj = machine
          prop_elems[..-2].each do |elem_prop|
            obj = obj.send("#{elem_prop}")
          end
          obj.send("#{prop_elems[-1]}=", value)
        end
      end

      machine.vm.synced_folder ".", "/vagrant", type: "sshfs"

      machine.vm.provider :libvirt do |libvirt|
        libvirt_def.each do |prop, value|
          libvirt.send("#{prop}=", value)
        end
      end

      machine.vm.provision "ansible" do |ansible|
        ansible.playbook = "ansible/#{mname}.yml"
        ansible.config_file = "ansible/ansible.cfg"
      end
    end
  end
end
