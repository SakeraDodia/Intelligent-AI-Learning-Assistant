import "./Roadmap.css";

import { useState } from "react";

import {
  Target,
  Rocket,
  BookOpen,
  Trophy
} from "lucide-react";

import { generateRoadmap } from "../../services/api";

function Roadmap() {

  const [generated, setGenerated] =
    useState(false);

  const [topic, setTopic] =
    useState("");

  const [duration, setDuration] =
    useState("3 Months");

  const [currentLevel, setCurrentLevel] =
    useState("Beginner");

  const [studyTime, setStudyTime] =
    useState("2 hours per day");

  const [loading, setLoading] =
    useState(false);

  const [roadmap, setRoadmap] =
    useState("");

  const [roadmapData, setRoadmapData] =
    useState([]);


  // ======================================================
  // GENERATE ROADMAP
  // ======================================================

  const handleGenerateRoadmap = async () => {

    if (!topic.trim() || loading) {
      return;
    }

    setLoading(true);

    try {

      const data =
        await generateRoadmap(
          topic,
          currentLevel,
          studyTime,
          duration
        );


      const response =
        data.roadmap ||
        data.response ||
        data.content ||
        "";


      setRoadmap(response);


      // If backend returns structured phases
      if (Array.isArray(data.phases)) {

        setRoadmapData(
          data.phases
        );

      } else {

        setRoadmapData([]);

      }


      setGenerated(true);

    } catch (error) {

      console.error(
        "Roadmap API Error:",
        error
      );

      alert(
        "Unable to generate roadmap. Please check the backend."
      );

    } finally {

      setLoading(false);

    }
  };


  // ======================================================
  // GENERATE AGAIN
  // ======================================================

  const handleGenerateAgain = () => {

    setGenerated(false);

    setRoadmap("");

    setRoadmapData([]);

  };


  return (

    <div className="roadmap-page">

      {!generated ? (

        <div className="roadmap-card">

          <Target size={70} />

          <h2>
            AI Roadmap Generator
          </h2>

          <p>
            Generate a learning roadmap
            for any career goal
          </p>


          <input
            type="text"
            placeholder="Goal (React Developer)"
            value={topic}
            onChange={(e) =>
              setTopic(e.target.value)
            }
          />


          <select
            value={duration}
            onChange={(e) =>
              setDuration(
                e.target.value
              )
            }
          >

            <option>
              3 Months
            </option>

            <option>
              6 Months
            </option>

            <option>
              12 Months
            </option>

          </select>


          <select
            value={currentLevel}
            onChange={(e) =>
              setCurrentLevel(
                e.target.value
              )
            }
          >

            <option>
              Beginner
            </option>

            <option>
              Intermediate
            </option>

            <option>
              Advanced
            </option>

          </select>


          <select
            value={studyTime}
            onChange={(e) =>
              setStudyTime(
                e.target.value
              )
            }
          >

            <option>
              1 hour per day
            </option>

            <option>
              2 hours per day
            </option>

            <option>
              3 hours per day
            </option>

            <option>
              4+ hours per day
            </option>

          </select>


          <button
            onClick={
              handleGenerateRoadmap
            }
            disabled={
              loading ||
              !topic.trim()
            }
          >

            {loading
              ? "Generating..."
              : "Generate Roadmap"}

          </button>

        </div>

      ) : (

        <div className="roadmap-container">

          <div className="roadmap-header">

            <h2>
              {topic} Roadmap
            </h2>


            <button
              onClick={
                handleGenerateAgain
              }
            >

              Generate Again

            </button>

          </div>


          {/* STRUCTURED ROADMAP */}

          {roadmapData.length > 0 ? (

            roadmapData.map(
              (phase, index) => (

                <div
                  className="milestone-card"
                  key={index}
                >

                  {index === 0 ? (
                    <BookOpen size={24} />
                  ) : index ===
                    roadmapData.length - 1 ? (
                    <Trophy size={24} />
                  ) : (
                    <Rocket size={24} />
                  )}


                  <div>

                    <h3>
                      {phase.title ||
                        phase.phase ||
                        `Phase ${index + 1}`}
                    </h3>

                    <p>
                      {phase.description ||
                        phase.topics ||
                        phase.content ||
                        ""}
                    </p>

                  </div>


                  <div className="progress">

                    {phase.progress ||
                      `${Math.round(
                        ((index + 1) /
                          roadmapData.length) *
                          100
                      )}%`}

                  </div>

                </div>

              )
            )

          ) : (

            /* TEXT ROADMAP */

            <div className="milestone-card">

              <BookOpen size={24} />

              <div>

                <h3>
                  AI Generated Roadmap
                </h3>

                <p
                  style={{
                    whiteSpace:
                      "pre-wrap"
                  }}
                >
                  {roadmap}
                </p>

              </div>

            </div>

          )}

        </div>

      )}

    </div>

  );
}

export default Roadmap;