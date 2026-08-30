"""The exercise schema: one record per exercise, equipment resolved by merge.

See DESIGN.md section 1. Each `Exercise` carries every equipment variant it
supports as a single record — `equipment_options` lists the valid combos,
`overrides` holds only the fields that differ per combo — rather than one
record per variant, to avoid the two copies drifting apart over edits.
"""

from dataclasses import asdict, dataclass, field

from combocizes.constants import (
    BODY_POSITIONS,
    BODY_REGIONS,
    DUMBBELL_FLAGS,
    EQUIPMENT_FLAGS,
    EQUIPMENT_PHRASES,
    IMPACT_LEVELS,
    MAT_ORIENTATIONS,
    MOVEMENT_PATTERNS,
    MOVER_DIRECTIONS,
    MOVER_LOCATIONS,
    MUSCLE_GROUPS,
    SINGLE_MODIFIER,
)

EquipmentCombo = dict[str, bool]
ComboKey = tuple[tuple[str, bool], ...]


def equipment_combo_key(equipment: EquipmentCombo) -> ComboKey:
    """Normalize an equipment combo into a hashable, order-independent key.

    Args:
        equipment: Per-category flags, e.g. `{"heavy_dumbbells": True}`. The
            empty dict `{}` is a valid combo, meaning no equipment (bodyweight).

    Returns:
        The flags as a sorted tuple of `(flag, value)` pairs.
    """
    return tuple(sorted(equipment.items()))


@dataclass(frozen=True)
class BodyPosition:
    """One valid start/end whole-body-stance pair for an exercise.

    Args:
        start: Whole-body stance at the start of the rep.
        end: Whole-body stance at the end of the rep. Equal to `start` for
            the common case of an exercise that returns to where it began
            (e.g. a curl held kneeling); different only when the rep itself
            carries the student's stance from one whole-body position to
            another (e.g. a reverse lunge: `standing_narrow` -> `lunge`).
    """

    start: str
    end: str

    @classmethod
    def held(cls, position: str) -> "BodyPosition":
        """A stance that doesn't change over the rep (`start == end`)."""
        return cls(position, position)


@dataclass
class PrimaryCue:
    """The cue spoken once, on an exercise's first appearance in a class.

    Assembled at render time into:
    `"{breath}, {exercise_name}, {action} {moved_object} {direction}."`

    Args:
        breath: E.g. "Exhale".
        action: The verb, e.g. "drive".
        action_pool_key: Key into a shared synonym pool for verb variety.
        direction: Fixed, exercise-specific free text.

    Note:
        The moved-object noun isn't authored here — `resolve_moved_object`
        derives it from `Exercise.mover` and the chosen equipment.
    """

    breath: str
    action: str
    action_pool_key: str
    direction: str


@dataclass
class Exercise:
    """A single exercise, covering every equipment variant it supports.

    Args:
        name: Unique exercise name.
        movement_pattern: One of `combocizes.constants.MOVEMENT_PATTERNS`.
        body_region: One of `combocizes.constants.BODY_REGIONS`.
        muscle_group: One of `combocizes.constants.MUSCLE_GROUPS`.
        body_positions: The whole-body stance(s) this exercise can be done
            from, as start/end pairs, e.g.
            `[BodyPosition.held("standing_narrow"), BodyPosition.held("kneeling")]`.
            Most exercises hold one stance throughout (`BodyPosition.held`
            covers that: `start == end`); a handful genuinely transition
            (e.g. a reverse lunge: `BodyPosition("standing_narrow",
            "lunge")`). A list, not a single pair, since some exercises
            validly work from several alternative stances (e.g. a hammer
            curl done standing_narrow, standing_wide, kneeling, or from a
            lunge) — purely additive, unlike equipment, since cue text
            doesn't change based on stance. Must list at least one pair,
            each `.start`/`.end` drawn from
            `combocizes.constants.BODY_POSITIONS`.
        unilateral: Whether the exercise works one side at a time.
        impact: One of `combocizes.constants.IMPACT_LEVELS`.
        equipment_options: Valid equipment combos for this exercise, e.g.
            `[{"heavy_dumbbells": True}, {"heavy_dumbbells": True, "single": True}]`.
            Must list at least one combo, but a combo may be the empty dict
            `{}` — that's a valid "no equipment" (bodyweight) entry, not an
            omission.
        mover: What's executing the movement — a body part (e.g. `"leg"`),
            independent of which equipment is selected, or `"equipment"`
            when the cue should name the held equipment instead (e.g. a
            curl). Must be a key in `combocizes.constants.MOVER_LOCATIONS`.
            Drives `resolve_moved_object`.
        location_start: `mover`'s physical location at the start of the
            rep (e.g. `"hanging"`, `"shoulder"`, `"lunge"`). Must be one of
            `combocizes.constants.MOVER_LOCATIONS[mover]`.
        location_end: `mover`'s location at the end of the rep. Same
            vocabulary as `location_start`.
        direction_start: Which way `mover` is oriented at the start of the
            rep — grip for `"equipment"` (e.g. `"palms_in"`), step
            direction for `"leg"` (e.g. `"back"`), rotation side for
            `"torso"` (e.g. `"left"`). Required, but `None` is a valid
            value — most movers have no direction axis at all (only
            `"equipment"`, `"leg"`, and `"torso"` have an entry in
            `combocizes.constants.MOVER_DIRECTIONS`), and even for those,
            most locations don't need a stated direction. When not `None`,
            must be one of `MOVER_DIRECTIONS[mover]`. Never inferred from
            `direction_end` — the two are independently authored, since a
            rep's start and end can genuinely face different ways (a
            reverse lunge starts facing `"forward"` and ends `"back"`).
        direction_end: Same vocabulary and independence as `direction_start`,
            at the end of the rep.
        primary_cue: The cue said once, on first appearance.
        mat_orientation_start: Which way the student faces on the mat at
            the start of the rep. One of `combocizes.constants.MAT_ORIENTATIONS`.
            Defaults to `"front"` — only exercises that actually turn (e.g.
            a plyo drill pivoting to face right) need to set this.
        mat_orientation_end: Same vocabulary, at the end of the rep.
            Defaults to `"front"`.
        overrides: Per-combo field overrides, keyed by `equipment_combo_key`.
            Only fields that differ from the base need appear.
        own_refinement_cues: Exercise-specific cues too particular to
            generalize into the shared bank. Shared cues are assigned the
            other way around — via `RefinementCue.exercise_ids` in
            `combocizes.cues.build_cue_bank()` — not referenced here.

    Raises:
        ValueError: If any classification field, equipment flag, or override
            key isn't drawn from its known set.
    """

    name: str
    movement_pattern: str
    body_region: str
    muscle_group: str
    body_positions: list[BodyPosition]
    unilateral: bool
    impact: str
    equipment_options: list[EquipmentCombo]
    mover: str
    location_start: str
    location_end: str
    direction_start: str | None
    direction_end: str | None
    primary_cue: PrimaryCue
    mat_orientation_start: str = "front"
    mat_orientation_end: str = "front"
    overrides: dict[ComboKey, dict] = field(default_factory=dict)
    own_refinement_cues: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._validate_classification_fields()
        self._validate_body_positions()
        self._validate_equipment_options()
        self._validate_overrides()
        self._validate_mover_location_and_direction()
        self._validate_mat_orientation()

    def _validate_classification_fields(self) -> None:
        checks = [
            ("movement_pattern", self.movement_pattern, MOVEMENT_PATTERNS),
            ("body_region", self.body_region, BODY_REGIONS),
            ("muscle_group", self.muscle_group, MUSCLE_GROUPS),
            ("impact", self.impact, IMPACT_LEVELS),
        ]
        for field_name, value, allowed in checks:
            if value not in allowed:
                raise ValueError(
                    f"{self.name}: invalid {field_name} {value!r}, expected one of {allowed}"
                )

    def _validate_body_positions(self) -> None:
        if not self.body_positions:
            raise ValueError(f"{self.name}: body_positions must list at least one position")
        unknown = {
            value
            for pair in self.body_positions
            for value in (pair.start, pair.end)
            if value not in BODY_POSITIONS
        }
        if unknown:
            raise ValueError(
                f"{self.name}: invalid body_positions {sorted(unknown)}, "
                f"expected values from {BODY_POSITIONS}"
            )

    def _validate_equipment_options(self) -> None:
        # `equipment_options` must be non-empty, but an entry may itself be
        # the empty dict `{}` — that's a valid "no equipment" combo.
        if not self.equipment_options:
            raise ValueError(f"{self.name}: equipment_options must list at least one combo")
        known_flags = {*EQUIPMENT_FLAGS, SINGLE_MODIFIER}
        for combo in self.equipment_options:
            unknown = set(combo) - known_flags
            if unknown:
                raise ValueError(f"{self.name}: unknown equipment flag(s) {unknown} in {combo!r}")
            if combo.get(SINGLE_MODIFIER) and not any(combo.get(flag) for flag in DUMBBELL_FLAGS):
                raise ValueError(
                    f"{self.name}: {SINGLE_MODIFIER!r} requires a dumbbell flag in {combo!r}"
                )

    def _validate_overrides(self) -> None:
        known_combo_keys = {equipment_combo_key(combo) for combo in self.equipment_options}
        unknown = set(self.overrides) - known_combo_keys
        if unknown:
            raise ValueError(
                f"{self.name}: overrides key(s) {unknown} match no equipment_options combo"
            )

    def _validate_mover_location_and_direction(self) -> None:
        if self.mover not in MOVER_LOCATIONS:
            raise ValueError(
                f"{self.name}: invalid mover {self.mover!r}, "
                f"expected one of {list(MOVER_LOCATIONS)}"
            )
        allowed_locations = MOVER_LOCATIONS[self.mover]
        for field_name, value in [
            ("location_start", self.location_start),
            ("location_end", self.location_end),
        ]:
            if value not in allowed_locations:
                raise ValueError(
                    f"{self.name}: invalid {field_name} {value!r} for mover {self.mover!r}, "
                    f"expected one of {allowed_locations}"
                )

        allowed_directions = MOVER_DIRECTIONS.get(self.mover, [])
        for field_name, value in [
            ("direction_start", self.direction_start),
            ("direction_end", self.direction_end),
        ]:
            if value is not None and value not in allowed_directions:
                raise ValueError(
                    f"{self.name}: invalid {field_name} {value!r} for mover {self.mover!r}, "
                    f"expected None or one of {allowed_directions}"
                )

    def _validate_mat_orientation(self) -> None:
        for field_name, value in [
            ("mat_orientation_start", self.mat_orientation_start),
            ("mat_orientation_end", self.mat_orientation_end),
        ]:
            if value not in MAT_ORIENTATIONS:
                raise ValueError(
                    f"{self.name}: invalid {field_name} {value!r}, "
                    f"expected one of {MAT_ORIENTATIONS}"
                )


def resolve_exercise(exercise: Exercise, equipment: EquipmentCombo) -> dict:
    """Resolve an exercise's fields for one chosen equipment combo.

    Args:
        exercise: The exercise to resolve.
        equipment: The equipment combo actually chosen, e.g. `{"heavy_dumbbells": True}`.

    Returns:
        The exercise's fields as a dict, with the matching `overrides` entry
        (if any) shallow-merged on top of the base fields.
    """
    combo_key = equipment_combo_key(equipment)
    return {**asdict(exercise), **exercise.overrides.get(combo_key, {})}


def resolve_moved_object(exercise: Exercise, equipment: EquipmentCombo) -> str:
    """Derive the moved-object noun for an exercise's primary cue.

    Args:
        exercise: The exercise to resolve.
        equipment: The equipment combo actually chosen.

    Returns:
        If `exercise.mover` is `"equipment"`, the phrase from
        `combocizes.constants.EQUIPMENT_PHRASES` for whichever equipment
        flag is set, singularized (trailing "s" dropped) if `single` is
        also set. Otherwise `"your {mover}"` — e.g. a lunge (`mover:
        "leg"`) always resolves to `"your leg"`, since the dumbbells stay
        racked; a curl (`mover: "equipment"`) resolves to `"your
        dumbbells"`, or `"your dumbbell"` for the single-dumbbell combo.

    Raises:
        KeyError: If `mover` is `"equipment"` but no flag in `equipment`
            has a known phrase (e.g. a bodyweight combo).
    """
    if exercise.mover != "equipment":
        return f"your {exercise.mover}"

    for flag in EQUIPMENT_FLAGS:
        if equipment.get(flag) and flag in EQUIPMENT_PHRASES:
            phrase = EQUIPMENT_PHRASES[flag]
            return phrase.removesuffix("s") if equipment.get(SINGLE_MODIFIER) else phrase

    raise KeyError(f"{exercise.name}: no equipment phrase for combo {equipment!r}")
