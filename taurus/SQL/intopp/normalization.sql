UPDATE motion_exchange
SET motion_exchange=motion_exchange*(
    (SELECT sum(sources) FROM sd)/
    (SELECT sum(motion_exchange) FROM motion_exchange)
)

