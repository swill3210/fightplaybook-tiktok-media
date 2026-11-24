import React from 'react';
import { Composition } from 'remotion';
import { LiverVideo } from './Video';
import TL from '../public/timeline.json';
export const Root: React.FC = () => <Composition id="Liver" component={LiverVideo} durationInFrames={TL.frames} fps={30} width={1920} height={1080} />;
