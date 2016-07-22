Feature: Paasta native mesos framework
  Scenario: we can start a service
    Given a working paasta cluster, with docker registry docker.io
      And a new paasta_native config to be deployed, with 3 instances
     When we start a paasta_native scheduler
     Then it should eventually start 3 tasks

  Scenario: native_mesos_scheduler.main() works
    Given a working paasta cluster, with docker registry docker.io
      And a fresh soa_dir
      And paasta_native-cluster.yaml and deployments.json files for service foo with instance one
      And paasta_native-cluster.yaml and deployments.json files for service bar with instance two
      And paasta_native-cluster.yaml and deployments.json files for service baz with instance three
     When we run native_mesos_scheduler.main()
     Then there should be a framework registered with name paasta foo.one
     Then there should be a framework registered with name paasta bar.two
     Then there should be a framework registered with name paasta baz.three

  Scenario: reuse same framework ID
    Given a working paasta cluster
      And a new paasta_native config to be deployed, with 1 instances
     When we start a paasta_native scheduler
     Then there should be a framework registered with name paasta fake_service.fake_instance
     When we stop that framework without terminating
      And we start a paasta_native scheduler
     Then there should be a framework registered with name paasta fake_service.fake_instance
      And it should have the same ID as before

  Scenario: new framework ID after termination
    Given a working paasta cluster
      And a new paasta_native config to be deployed, with 1 instances
     When we start a paasta_native scheduler
     Then there should be a framework registered with name paasta fake_service.fake_instance
     When we terminate that framework
     Then there should not be a framework registered with name paasta fake_service.fake_instance
     When we start a paasta_native scheduler
     Then there should be a framework registered with name paasta fake_service.fake_instance
      And it should have a different ID than before

  Scenario: native_mesos_scheduler starts new tasks when config changes
    Given a working paasta cluster, with docker registry docker.io
      And a new paasta_native config to be deployed, with 3 instances
     When we start a paasta_native scheduler
     Then it should eventually start 3 tasks
     When we change the config
     Then it should eventually start 6 tasks