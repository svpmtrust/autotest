
package { ["git", "apache2"]:
  ensure => present
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

service { "apache2":
  ensure => running,
  subscribe => [Exec["a2edav"], Exec["a2edav_fs"]]
}

