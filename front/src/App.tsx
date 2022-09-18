import React, { useEffect, useState } from 'react';
import './App.css';
import { getDetails, getSuggestions, getToken, setRelevance, sendMail } from './services/services';
import { Backdrop, Button, CircularProgress, Popover, TextField, Typography } from '@material-ui/core';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import { styled } from '@mui/material/styles';
import { reduceEachLeadingCommentRange } from 'typescript';
import Checkbox from '@mui/material/Checkbox';
import { FiMail } from 'react-icons/fi';

import ModalUnstyled from '@mui/base/ModalUnstyled';
import { Box } from '@mui/system';

const label = { inputProps: { 'aria-label': 'Checkbox demo' } };

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#19ad5c',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

const StyledModal = styled(ModalUnstyled)`
  position: fixed;
  z-index: 1300;
  right: 0;
  bottom: 0;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const Backdrop2 = styled('div')`
  z-index: -1;
  position: fixed;
  right: 0;
  bottom: 0;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.5);
`;

const style = {
  width: 400,
  bgcolor: 'white',
  border: '2px solid #000',
  p: 2,
  px: 4,
  pb: 3,
};

interface ISuggestion {
  index: number;
  control_name: string;
}

function App() {
  const [sentence, setSentence] = useState<string>("");
  const [suggestions, setSuggestions] = useState<ISuggestion[]>([]);
  const [open, setOpen] = useState<boolean>(false);
  const [details, setDetails] = useState<any>(null);
  const [relevantSuggestions, setRelevantSuggestions] = useState<{[key: number]: boolean}>({});
  const [look, setLook] = useState<boolean>(false);

  const handleClose = () => setOpen(false);

  useEffect(() => {
    getToken("http://127.0.0.1:5000/generate-token")
  }, []);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSentence(event.target.value);
  }

  const fetchSuggestions = async () => {
    const res: ISuggestion[] = await getSuggestions("http://127.0.0.1:5000/suggestion", sentence);
    const newState: { [key: number]: boolean } = {};
    res.forEach((item) => { newState[item.index] = false });
    setRelevantSuggestions(newState);
    setSuggestions(res);
    setLook(true)
  }

  const handlePopoverOpen = async (index: number) => {
    const res = await getDetails("http://127.0.0.1:5000/details", index);
    setOpen(true);
    setDetails(res);
  }

  const onCheckboxChange = (index: number, value: boolean) => {
    const newState = { ...relevantSuggestions };
    newState[index] = value;

    setRelevantSuggestions(newState);
  }

  const submitRelevants = async () => {
    const payload = Object.keys(relevantSuggestions).filter((key) => relevantSuggestions[Number(key)]).map((key) => Number(key));
    setRelevance("http://127.0.0.1:5000/relevance", payload);
  }

  const submitMail = async () => {
    sendMail("http://127.0.0.1:5000/contact");
  }
  return (
    <div>
    <div className='first-block'>
      <h1>BNP Search Engine</h1>
      </div>
    
    <div className='background'>
        <div className="inputsearch">
          <TextField fullWidth label="What are you looking for?" variant="outlined" type="search" onChange={handleChange}/>
          <button onClick={fetchSuggestions}>Search</button>
        </div>
        
        {(suggestions && suggestions.length) ? <div className="results"><Stack spacing={4}>
            {
              suggestions.map((sug) =>
              <div key={sug.index}>

                <Item onClick={() => handlePopoverOpen(sug.index)}>
                  <Typography
                    key={sug.index}
                  >
                    {sug.control_name}
                  </Typography>
                </Item>
                <Checkbox {...label} checked={relevantSuggestions[sug.index]} onChange={(e) => onCheckboxChange(sug.index, e.target.checked)}/>
              </div>)
            }
            </Stack>
          </div> : null
        }
        {(suggestions.length===0 && look) ? <div className='nothing-found'><p>Nothing Found &#128533;</p></div>:null
        }
        {details && <StyledModal
          aria-labelledby="unstyled-modal-title"
          aria-describedby="unstyled-modal-description"
          open={open}
          onClose={handleClose}
          BackdropComponent={Backdrop2}
        >
          <Box sx={style}>
            {/* <h2 id="unstyled-modal-title">{JSON.stringify(details)}</h2>
            <p id="unstyled-modal-description">Aliquid amet deserunt earum!</p> */}
            {Object.keys(details).map((key) => <h4 key={String(key)}>{key} - {details[key]}</h4>)}
          </Box>
        </StyledModal>}
    </div>
    <div className='submit-button'>
      <Button onClick={submitRelevants}>
        Submit Feedback
      </Button>
    </div>
    
    <div className='mail_button'>
    <Button onClick={submitMail}>
      <h3> Contact <FiMail /> </h3>
    </Button>
      {/* <Button onClick={submitMail}>
        Send mail
      </Button> */}
    </div>

    </div>
  );
}

export default App;
