
package { [ "git", "wget", "apache2", "apache2-utils", "apg" ]:
  ensure => present
}

file { "/etc/apache2/mods-enabled/git.conf":
    ensure => present,
    source => '/etc/puppet/gitserver/git.conf',
    require => Package["apache2"]
}

file { "/opt/git":
  ensure => directory,
  owner => 'www-data',
  require => Package["apache2"]
}

exec { "a2ecgi":
  command => 'a2enmod cgi',
  path => ['/bin','/usr/bin','/usr/sbin'],
  require => Package["apache2"]
}

service { "apache2":
  ensure => running,
  subscribe => Exec["a2ecgi"]
}

