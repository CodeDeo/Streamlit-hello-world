with st.expander("View dice rolls", expanded=True):
            st.table([
                {"Roll": index + 1, "Kept dice": " + ".join(map(str, roll[1:])),
                 "Dropped": roll[0], "Total": values[index]}
                for index, roll in enumerate(dice)
            ])
    else:
        values = STANDARD_ARRAY

    st.caption("Assign each score slot once. Slots with the same total are separate choices.")
    columns = st.columns(3)
    slots = [
        columns[index % 3].selectbox(
            ability, range(len(values)), index=index, key=f"ability_{index}",
            format_func=lambda slot: f"{values[slot]} (slot {slot + 1})",
        )
        for index, ability in enumerate(ABILITIES)
    ]
    if len(set(slots)) != len(ABILITIES):
        st.warning("Assign a different slot to each ability to see your character summary.")
        return None
    return [values[slot] for slot in slots]


def show_character(name, character_class, ancestry, scores):
    rows, hp, initiative, speed = character_stats(character_class, ancestry, scores)
    st.header(name)
    st.caption(f"Level 1 · {ancestry} · {character_class}")
    health, turn, movement, proficiency = st.columns(4)
    health.metric("Hit points", hp)
    turn.metric("Initiative", f"{initiative:+d}")
    movement.metric("Walking speed", f"{speed} ft")
    proficiency.metric("Proficiency bonus", "+2")
    st.subheader("Ability scores")
    st.dataframe(rows, hide_index=True)
    st.bar_chart(rows, x="Ability", y="Score", horizontal=True)
    summary = [
        name, f"Level 1 {ancestry} {character_class}",
        f"HP {hp} | Initiative {initiative:+d} | Speed {speed} ft | Proficiency +2", "",
        *[
            f"{row['Ability']}: {row['Score']} ({row['Modifier']:+d}), "
            f"saving throw {row['Saving throw']:+d}"
            for row in rows
        ],
        "", ATTRIBUTION,
    ]
    st.download_button("Download character summary", "\n".join(summary),
                       file_name="character-summary.txt", mime="text/plain")


def main():
    st.set_page_config(page_title="Character Forge", page_icon="🎲", layout="wide")
    st.title("Character Forge")
    st.write("Build a level-one D&D character using the 2014 fifth-edition rules.")
    with st.sidebar:
        st.header("Character details")
        name = st.text_input("Character name", max_chars=60).strip() or "Unnamed adventurer"
        character_class = st.selectbox("Class", tuple(CLASSES), index=4)
        ancestry = st.selectbox("Ancestry", tuple(ANCESTRIES))
        st.caption("The summary covers core stats. Choose skills, equipment, and spells separately.")
    st.header("Assign ability scores")
    scores = select_scores()
    if scores is not None:
        show_character(name, character_class, ancestry, scores)
    with st.expander("Rules attribution"):
        st.write(ATTRIBUTION)


if __name__ == "__main__":
    main()
