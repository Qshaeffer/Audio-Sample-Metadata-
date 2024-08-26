CREATE TABLE sample_description_t AS
SELECT 
    s.name AS sample_name,
    COALESCE(
        NULLIF(
            (
                COALESCE(
                    (SELECT GROUP_CONCAT(DISTINCT t2.tag_name)
                     FROM sample_tag_t st2
                     JOIN tag_t t2 ON st2.tag_id = t2._id
                     WHERE st2.sample_id = s._id
                    ),
                    ''
                ) || 
                CASE 
                    WHEN (SELECT COUNT(*) FROM sample_tag_t st3 WHERE st3.sample_id = s._id) > 0 
                    THEN ', ' 
                    ELSE '' 
                END ||
                COALESCE(i.name, '') ||
                CASE 
                    WHEN i.name IS NOT NULL THEN ', ' 
                    ELSE '' 
                END ||
                CASE s.one_shot_loop
                    WHEN 1 THEN 'One shot'
                    WHEN 2 THEN 'Loop'
                    WHEN 3 THEN 'Long'
                    ELSE 'Unknown'
                END
            ),
            ''
        ),
        'No description'
    ) AS description
FROM 
    sample_t s
LEFT JOIN 
    instrument_t i ON s.instrument_id = i._id
GROUP BY 
    s._id, s.name, i.name, s.one_shot_loop		
