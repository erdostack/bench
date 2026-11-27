# Firmware rollout rings

Every sensor is in exactly one ring: canary, early or broad. The rollout tool reads
`rings.member_count` to size each wave (it schedules gateway airtime from it) and stops a wave when
the number of devices that report the new version reaches `member_count`. A count that is off means a
wave that never completes or one that finishes early.
