## `Nexus` Cluster


| Gateway | Master Nodes | Worker Nodes | Networking | Storage |
|:---: |:---: | :---: | :---: | :---: |
| :material-check-circle: | :material-check-circle: |:octicons-x-circle-16: | :material-check-circle: | :material-check-circle: |

``` vegalite
--8<-- "docs/hpc/status-worker.json"
```
!!! failure "Cluster Health"


## Gateway

``` vegalite
--8<-- "docs/hpc/status-gateway.json"
```

??? success "Gateway Node"
    ??? success "nexusagateway0.chapman.edu"
        ??? success "coming soon"
            TODO: coming soon


## Masters

``` vegalite
--8<-- "docs/hpc/status-master.json"
```

??? success "Master Nodes"
    ??? success "master0.chapman.edu"
        ??? success "coming soon"
            TODO: coming soon



## Workers

``` vegalite
--8<-- "docs/hpc/status-worker.json"
```

??? failure "Worker Nodes"
    ??? warning "nexusworker0.chapman.edu"
        ??? success "nvidia-smi"
            ``` title="nvidia-smi" linenums="1"
            --8<-- "docs/t3/nx-w0-nvidia-smi"
            ```

        ??? warning "nvsm health"
            ``` title="nvsm show health" linenums="1" hl_lines="132"
            --8<-- "docs/t3/nx-w0-nvsm-health"
            ```

        ??? success "dcgmi"
            ``` title="dcgmi diag -r 3 -p diagnostic.test_duration=30.0" linenums="1"
            --8<-- "docs/t3/nx-w0-dcgmi"
            ```


        ??? warning "stress test"
            ``` title="nvsm stress-test --no-prompt --force" linenums="1" hl_lines="15 19"
            --8<-- "docs/t3/nx-w0-stress-test"
            ```


        ??? success "stress test log"
            ``` title="sudo cat /var/nvsmlog/nvsm/StressTestLog2024-04-28T21:21:32-05:00.nvsmlog" linenums="1"
            --8<-- "docs/t3/nx-w0-stress-test-log"
            ```

    ??? failure "nexusworker1.chapman.edu"
        ??? success "nvidia-smi"
            ``` title="nvidia-smi" linenums="1"
            --8<-- "docs/t3/nx-w1-nvidia-smi"
            ```

        ??? success "nvsm health"
            ``` title="nvsm show health" linenums="1"
            --8<-- "docs/t3/nx-w1-nvsm-health"
            ```

        ??? failure "dcgmi"
            ``` title="dcgmi diag -r 3 -p diagnostic.test_duration=30.0" linenums="1" hl_lines="21"
            --8<-- "docs/t3/nx-w1-dcgmi"
            ```


        ??? failure "stress test"
            ``` title="nvsm stress-test --no-prompt --force" linenums="1" hl_lines="15 19"
            --8<-- "docs/t3/nx-w1-stress-test"
            ```


        ??? success "stress test log"
            ``` title="sudo cat /var/nvsmlog/nvsm/StressTestLog2024-04-28T21:21:32-05:00.nvsmlog" linenums="1"
            --8<-- "docs/t3/nx-w1-stress-test-log"
            ```

    ??? failure "nexusworker2.chapman.edu"
        ??? success "nvidia-smi"
            ``` title="nvidia-smi" linenums="1"
            --8<-- "docs/t3/nx-w2-nvidia-smi"
            ```

        ??? success "nvsm health"
            ``` title="nvsm show health" linenums="1"
            --8<-- "docs/t3/nx-w2-nvsm-health"
            ```

        ??? success "dcgmi"
            ``` title="dcgmi diag -r 3 -p diagnostic.test_duration=30.0" linenums="1"
            --8<-- "docs/t3/nx-w2-dcgmi"
            ```


        ??? failure "stress test"
            ``` title="nvsm stress-test --no-prompt --force" linenums="1" hl_lines="15 19"
            --8<-- "docs/t3/nx-w2-stress-test"
            ```


        ??? success "stress test log"
            ``` title="sudo cat /var/nvsmlog/nvsm/StressTestLog2024-04-28T21:21:32-05:00.nvsmlog" linenums="1"
            --8<-- "docs/t3/nx-w2-stress-test-log"
            ```

    ??? failure "nexusworker3.chapman.edu"
        ??? success "nvidia-smi"
            ``` title="nvidia-smi" linenums="1"
            --8<-- "docs/t3/nx-w3-nvidia-smi"
            ```

        ??? warning "nvsm health"
            ``` title="nvsm show health" linenums="1" hl_lines="13 74"
            --8<-- "docs/t3/nx-w3-nvsm-health"
            ```

        ??? failure "dcgmi"
            ``` title="dcgmi diag -r 3 -p diagnostic.test_duration=30.0" linenums="1" hl_lines="21"
            --8<-- "docs/t3/nx-w3-dcgmi"
            ```

        ??? failure "stress test"
            ``` title="nvsm stress-test --no-prompt --force" linenums="1" hl_lines="15 19"
            --8<-- "docs/t3/nx-w3-stress-test"
            ```


        ??? success "stress test log"
            ``` title="sudo cat /var/nvsmlog/nvsm/StressTestLog2024-04-28T21:21:32-05:00.nvsmlog" linenums="1"
            --8<-- "docs/t3/nx-w3-stress-test-log"
            ```


## Networking

``` vegalite
--8<-- "docs/hpc/status-master.json"
```

??? success "Networking subsystem"
    TODO: coming soon


## Storage

``` vegalite
--8<-- "docs/hpc/status-master.json"
```

??? success "Storage subsystem"
    TODO: coming soon


