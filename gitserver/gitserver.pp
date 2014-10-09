
package { [ "git", "wget" ]:
  ensure => present
}

package { "apache2":
  ensure => "2.2.29"
}

file { "/etc/apache2/conf.d/git":
    ensure => present,
    source => '/etc/puppet/git.conf',
    require => Package["apache2"]
}

file { "/opt/git":
  ensure => directory,
  owner => 'www-data',
  require => Package["apache2"]
}

exec { "a2edav":
  command => 'a2enmod dav',
  path => ['/bin','/usr/bin','/usr/sbin'],
  require => Package["apache2"]
}

exec { "a2edav_fs":
  command => 'a2enmod dav_fs',
  path => ['/bin','/usr/bin','/usr/sbin'],
  require => Package["apache2"]
}

exec { "random_passwords":
  command => "wget 'https://www.random.org/passwords/?num=100&len=8&format=plain&rnd=new' -O random_passwords",
  creates => "random_passwords"
}

service { "apache2":
  ensure => running,
  subscribe => [Exec["a2edav"], Exec["a2edav_fs"]]
}


]