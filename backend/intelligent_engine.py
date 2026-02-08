from ast_analyzer import (
    analyze_project,
    analyze_code_string,
    suggest_optimized_code
)

from optimizer_engine import (
    rank_suggestions,
    generate_variants,
    explain_optimization
)

print("\n🧠 Code Intelligence Engine Ready\n")

while True:
    print("Choose input type:")
    print("1. Analyze project files")
    print("2. Analyze user-provided code")
    print("3. Exit")

    main_choice = input("\nEnter choice: ").strip()
    original_code = None

    if main_choice == "1":
        functions = analyze_project()

    elif main_choice == "2":
        print("\nPaste Python code below.")
        print("Type END on a new line when finished:\n")

        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)

        original_code = "\n".join(lines)
        functions = analyze_code_string(original_code)

        for f in functions:
            f["file"] = "User_Input_Code"

    elif main_choice == "3":
        print("Exiting Code Intelligence Engine")
        break

    else:
        print("Invalid choice\n")
        continue

    # ---------------- ANALYSIS MENU ----------------

    while True:
        print("\nAnalysis Options:")
        print("1. Show all functions / blocks")
        print("2. Functions / blocks with loops")
        print("3. Most complex function / block")
        print("4. Check recursion")
        print("5. Detailed analysis + optimization")
        print("6. Back to main menu")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            for f in functions:
                print(f"{f['file']} → {f['name']}")

        elif choice == "2":
            for f in functions:
                if f["loops"] > 0:
                    print(f"{f['name']} (loops: {f['loops']})")

        elif choice == "3":
            most_complex = max(functions, key=lambda x: x["complexity"])
            print(f"\nMost complex: {most_complex['name']}")
            print(f"Cyclomatic Complexity: {most_complex['complexity']}")

        elif choice == "4":
            recursive_funcs = [f for f in functions if f["recursive"]]
            if recursive_funcs:
                for f in recursive_funcs:
                    print(f"{f['name']} is recursive")
            else:
                print("No recursive functions found")

        elif choice == "5":
            name = input("\nEnter function / block name: ").strip()
            found = False

            for f in functions:
                if f["name"] == name:
                    found = True

                    print("\n📊 Detailed Analysis")
                    print(f"File                  : {f['file']}")
                    print(f"Name                  : {f['name']}")
                    print(f"Loops                 : {f['loops']}")
                    print(f"Conditions            : {f['conditions']}")
                    print(f"Max Nesting Depth     : {f['max_depth']}")
                    print(f"Recursive             : {'Yes' if f['recursive'] else 'No'}")
                    print(f"Cyclomatic Complexity : {f['complexity']}")

                    if f["complexity"] <= 2:
                        level = "LOW"
                    elif f["complexity"] <= 4:
                        level = "MEDIUM"
                    else:
                        level = "HIGH"

                    print(f"Complexity Level      : {level}")

                    if f["reasons"]:
                        print("Reasons:")
                        for r in set(f["reasons"]):
                            print("-", r)

                    # -------- ADVANCED OPTIMIZATION --------
                    if original_code:
                        suggestions, _ = suggest_optimized_code(
                            original_code, f
                        )

                        if suggestions:
                            ranked = rank_suggestions(f, suggestions)

                            print("\n💡 Optimization Suggestions (Ranked):")
                            for score, text in ranked:
                                print(f"- {text} (impact score: {score})")

                            print("\n🧪 Optimized Code Variants:")
                            variants = generate_variants(original_code, f)
                            for idx, (label, variant) in enumerate(variants, 1):
                                print(f"\nVariant {idx} ({label}):")
                                print(variant)

                            print("\n🧠 Explanation:")
                            print(explain_optimization(f))
                        else:
                            print("\n✨ No safe optimizations suggested")

            if not found:
                print("Function / block not found")

        elif choice == "6":
            break

        else:
            print("Invalid option")
