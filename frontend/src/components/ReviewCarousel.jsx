import Slider from "react-slick";
import { Box, Typography, Paper, Rating } from "@mui/material";
import { ReplyAllRounded } from "@mui/icons-material";

import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";


export default function ReviewCarousel({ reviews }) {

const settings = {
  dots: true,
  infinite: true,
  speed: 500,
  slidesToShow: 1,
  slidesToScroll: 1,
  autoplay: true,
  arrows: true,
};

  return (
    <Box sx={{ maxWidth: 600, mx: "auto", mt: 4 }}>
    {reviews.length === 1 ? (
      <Paper sx={{ p: 3, m: 1 }}>
        <Typography variant="subtitle1">{reviews[0].name || "Anonymous"}</Typography>
        <Rating value={reviews[0].rating} readOnly />
        <Typography variant="body2" sx={{ mt: 1 }}>{reviews[0].comment}</Typography>
      </Paper>
    ) : (
      <Slider {...settings}>
        {reviews.map((r, i) => (
          <Paper key={i} sx={{ p: 3, m: 1 }}>
            <Typography variant="subtitle1">
              {r.name  || "Anonymous"} <ReplyAllRounded />
            </Typography>
            
            <Rating value={r.rating} readOnly />
            <Typography variant="body2" sx={{ mt: 1 }}>
              {r.comment}
            </Typography>
          </Paper>
        ))}
      </Slider>
    )}
    </Box>
  );
}
