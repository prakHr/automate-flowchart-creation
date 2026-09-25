import shutil
import subprocess


def create_flowchart(nodes, connections):

    results = []

    # Nodes
    for node_type, node_name, description in nodes:

        if description:
            results.append(
                f"{node_type:<10} {node_name:<15} {description}"
            )
        else:
            results.append(
                f"{node_type:<10} {node_name}"
            )

    results.append("")

    # Connections
    for source, arrow, target, label in connections:

        if label:
            results.append(
                f"{source:<10} {arrow:<5} {target:<10} {label}"
            )
        else:
            results.append(
                f"{source:<10} {arrow:<5} {target}"
            )

    return "\n".join(results)


def save_content_into_dfd_file(dfd_content, file_name):

    with open(file_name, "w", encoding="utf-8") as file:
        file.write(dfd_content)

    return "successfully saved!"


def create_flow_chart(file_name, out_file_name):

    # --------------------------------------------------------
    # Check Graphviz
    # --------------------------------------------------------

    dot_path = shutil.which("dot")

    if dot_path is None:

        print()
        print("ERROR: Graphviz is not installed or not in PATH.")
        print()
        print("Install it using:")
        print("  winget install Graphviz.Graphviz")
        print()
        print("Then restart PowerShell and run:")
        print("  dot -V")

        return None

    print()
    print("Graphviz found:")
    print(dot_path)

    # --------------------------------------------------------
    # Check data-flow-diagram
    # --------------------------------------------------------

    dfd_command = shutil.which("data-flow-diagram")

    if dfd_command is None:

        print()
        print("ERROR: data-flow-diagram command not found.")

        return None

    # --------------------------------------------------------
    # Generate SVG
    # --------------------------------------------------------

    result = subprocess.run(
        [
            dfd_command,
            file_name,
            "-o",
            out_file_name,
            "--no-graph-title"
        ],
        capture_output=True,
        text=True
    )

    return result


if __name__ == "__main__":

    nodes = [

        ("process", "Acquire", "Acquire data"),
        ("process", "Compute", ""),
        ("control", "Control", ""),
        ("entity", "Device", ""),
        ("store", "Config", "Configuration"),
        ("channel", "API", ""),
        ("control", "Control2", ""),
        
    ]

    connections = [

        ("Device", "->>", "Acquire", "continuous raw data"),
        ("Acquire", "-->", "Compute", "raw records"),
        ("Config", "<->", "Compute", "parameters"),
        ("Compute", "-->", "API", "records")
    ]

    # --------------------------------------------------------
    # Create DFD
    # --------------------------------------------------------

    dfd_content = create_flowchart(
        nodes,
        connections
    )

    print()
    print("Generated DFD:")
    print("=" * 70)
    print(dfd_content)
    print("=" * 70)

    # --------------------------------------------------------
    # Paths
    # --------------------------------------------------------

    file_name = (
       r"C:\Users\gprak\Downloads\Github Repos\a.dfd"
    )

    out_file_name = (
      r"C:\Users\gprak\Downloads\Github Repos\a.svg"
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    print()
    print(save_content_into_dfd_file(
        dfd_content,
        file_name
    ))

    # --------------------------------------------------------
    # Generate SVG
    # --------------------------------------------------------

    result = create_flow_chart(
        file_name,
        out_file_name
    )

    if result is None:
        raise SystemExit(1)

    print()
    print("DFD generation result:")
    print(result)

    if result.returncode == 0:

        print()
        print("========================================")
        print("SVG successfully generated!")
        print("========================================")
        print(out_file_name)

    else:

        print()
        print("SVG generation failed:")
        print(result.stderr)
