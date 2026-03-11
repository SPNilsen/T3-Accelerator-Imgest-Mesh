# Post Installation System Tests


!!! abstract "System Tests Results Executed by Trace3"
    For each system installed, the following are the results of
    tests as run by Trace3 after the installation. These are in
    accordance with nVIDIA User Manuals.


??? note "nexusworker0"
    ??? success "nvidia-smi"
        ``` title="nvidia-smi" linenums="1"
        --8<-- "../configs/nx-w0-nvidia-smi"
        ```

    ??? warning "nvsm health"
        ``` title="nvsm show health" linenums="1" hl_lines="132"
        --8<-- "docs/hpc/configs/nx-w0-nvsm-health"
        ```

    ??? success "dcgmi"
        ``` title="dcgmi diag -r 3 -p diagnostic.test_duration=30.0" linenums="1"
        --8<-- "docs/hpc/configs/nx-w0-dcgmi"
        ```


    ??? failure "stress test"
        ``` title="nvsm stress-test --no-prompt --force" linenums="1" hl_lines="15 19"
        --8<-- "docs/hpc/configs/nx-w0-stress-test"
        ```


    ??? success "stress test log"
        ``` title="sudo ca.v.nvsml.nv.StressTestLog2024-04-28T21:21:32-05:00.nvsmlog" linenums="1"
        --8<-- "docs/hpc/configs/nx-w0-stress-test-log"
        ```

??? note "nexusworker1"
    ??? success "nvidia-smi"
        ``` title="nvidia-smi" linenums="1"
        --8<-- "docs/hpc/configs/nx-w1-nvidia-smi"
        ```

    ??? success "nvsm health"
        ``` title="nvsm show health" linenums="1"
        --8<-- "docs/hpc/configs/nx-w1-nvsm-health"
        ```

    ??? failure "dcgmi"
        ``` title="dcgmi diag -r 3 -p diagnostic.test_duration=30.0" linenums="1" hl_lines="21"
        --8<-- "docs/hpc/configs/nx-w1-dcgmi"
        ```


    ??? failure "stress test"
        ``` title="nvsm stress-test --no-prompt --force" linenums="1" hl_lines="15 19"
        --8<-- "docs/hpc/configs/nx-w1-stress-test"
        ```


    ??? success "stress test log"
        ``` title="sudo ca.v.nvsml.nv.StressTestLog2024-04-28T21:21:32-05:00.nvsmlog" linenums="1"
        --8<-- "docs/hpc/configs/nx-w1-stress-test-log"
        ```

??? note "nexusworker2"
    ??? success "nvidia-smi"
        ``` title="nvidia-smi" linenums="1"
        --8<-- "docs/hpc/configs/nx-w2-nvidia-smi"
        ```

    ??? success "nvsm health"
        ``` title="nvsm show health" linenums="1"
        --8<-- "docs/hpc/configs/nx-w2-nvsm-health"
        ```

    ??? success "dcgmi"
        ``` title="dcgmi diag -r 3 -p diagnostic.test_duration=30.0" linenums="1"
        --8<-- "docs/hpc/configs/nx-w2-dcgmi"
        ```


    ??? failure "stress test"
        ``` title="nvsm stress-test --no-prompt --force" linenums="1" hl_lines="15 19"
        --8<-- "docs/hpc/configs/nx-w2-stress-test"
        ```


    ??? success "stress test log"
        ``` title="sudo ca.v.nvsml.nv.StressTestLog2024-04-28T21:21:32-05:00.nvsmlog" linenums="1"
        --8<-- "docs/hpc/configs/nx-w2-stress-test-log"
        ```

??? note "nexusworker3"
    ??? success "nvidia-smi"
        ``` title="nvidia-smi" linenums="1"
        --8<-- "docs/hpc/configs/nx-w3-nvidia-smi"
        ```

    ??? warning "nvsm health"
        ``` title="nvsm show health" linenums="1" hl_lines="13 74"
        --8<-- "docs/hpc/configs/nx-w3-nvsm-health"
        ```

    ??? failure "dcgmi"
        ``` title="dcgmi diag -r 3 -p diagnostic.test_duration=30.0" linenums="1" hl_lines="21"
        --8<-- "docs/hpc/configs/nx-w3-dcgmi"
        ```

    ??? failure "stress test"
        ``` title="nvsm stress-test --no-prompt --force" linenums="1" hl_lines="15 19"
        --8<-- "docs/hpc/configs/nx-w3-stress-test"
        ```


    ??? success "stress test log"
        ``` title="sudo ca.v.nvsml.nv.StressTestLog2024-04-28T21:21:32-05:00.nvsmlog" linenums="1"
        --8<-- "docs/hpc/configs/nx-w3-stress-test-log"
        ```
