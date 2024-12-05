import os
import sys
import UnityPy

srcDir = sys.argv[1] if sys.argv[1] else '.'
expDir = sys.argv[2] if sys.argv[2] else 'exported'
batDir = f'{expDir}/battle'
buiDir = f'{expDir}/build'

def readFromPathId(parent, list):
    try:
        return next(obj for obj in list if obj.read().path_id == parent['m_PathID']).read()
    except:
        return None

for file in os.listdir(srcDir):
    # try:
        # if file != 'char_002_amiya.ab': continue
        if not file.endswith('.ab'): continue

        env = UnityPy.load(os.path.join(srcDir, file))
        materials = []
        monobehaviours = []
        textassets = []
        texture2ds = []

        for obj in env.objects:
            match obj.type.name:
                case 'Material':
                    materials.append(obj)
                case 'MonoBehaviour':
                    monobehaviours.append(obj)
                case 'TextAsset':
                    textassets.append(obj)
                case 'Texture2D':
                    texture2ds.append(obj)

        count = 0
        for mono in monobehaviours:
            charA = mono.read()
            charATree = charA.read_typetree()
            if not (any(value not in charATree.keys() for value in ['_animations', '_spineScale'])): # Battle spine

                count += 1
                
                if(charATree.get('_front') and charATree.get('_back')): # Char has both front and back spine
                    fSkelA = readFromPathId(charATree['_front']['skeleton'], monobehaviours)
                    fSkelDA = readFromPathId(fSkelA.read_typetree()['skeletonDataAsset'], monobehaviours)
                    fSkelFile = readFromPathId(fSkelDA.read_typetree()['skeletonJSON'], textassets)
                    fAtlasA = readFromPathId(fSkelDA.read_typetree()['atlasAssets'][0], monobehaviours)
                    fAtlasFile = readFromPathId(fAtlasA.read_typetree()['atlasFile'], textassets)
                    fMats = readFromPathId(fAtlasA.read_typetree()['materials'][0], materials)
                    for tex in fMats.read_typetree()['m_SavedProperties']['m_TexEnvs']:
                        if tex[0] == '_AlphaTex':
                            fAlphaTex = readFromPathId(tex[1]['m_Texture'], texture2ds)
                        elif tex[0] == '_MainTex':
                            fMainTex = readFromPathId(tex[1]['m_Texture'], texture2ds)
                
                    bSkelA = readFromPathId(charATree['_back']['skeleton'], monobehaviours)
                    bSkelDA = readFromPathId(bSkelA.read_typetree()['skeletonDataAsset'], monobehaviours)
                    bSkelFile = readFromPathId(bSkelDA.read_typetree()['skeletonJSON'], textassets)
                    bAtlasA = readFromPathId(bSkelDA.read_typetree()['atlasAssets'][0], monobehaviours)
                    bAtlasFile = readFromPathId(bAtlasA.read_typetree()['atlasFile'], textassets)
                    bMats = readFromPathId(bAtlasA.read_typetree()['materials'][0], materials)
                    for tex in bMats.read_typetree()['m_SavedProperties']['m_TexEnvs']:
                        if tex[0] == '_AlphaTex':
                            bAlphaTex = readFromPathId(tex[1]['m_Texture'], texture2ds)
                        elif tex[0] == '_MainTex':
                            bMainTex = readFromPathId(tex[1]['m_Texture'], texture2ds)

                    charName = fMainTex.name
                    fDir = f'{batDir}/{charName}/front'
                    bDir = f'{batDir}/{charName}/back'
                    if not os.path.exists(expDir):
                        os.mkdir(expDir)
                    if not os.path.exists(batDir):
                        os.mkdir(batDir)
                    if not os.path.exists(f'{batDir}/{charName}'):
                        os.mkdir(f'{batDir}/{charName}')
                    if not os.path.exists(fDir):
                        os.mkdir(fDir)
                    if not os.path.exists(bDir):
                        os.mkdir(bDir)

                    open(f'{fDir}/{fSkelFile.name}', 'wb').write(fSkelFile.script)
                    open(f'{fDir}/{fAtlasFile.name}', 'wb').write(fAtlasFile.script)
                    if fAlphaTex is not None:
                        fAlphaTex.image.save(f'{fDir}/{fAlphaTex.name}.png')
                    fMainTex.image.save(f'{fDir}/{fMainTex.name}.png')

                    open(f'{bDir}/{bSkelFile.name}', 'wb').write(bSkelFile.script)
                    open(f'{bDir}/{bAtlasFile.name}', 'wb').write(bAtlasFile.script)
                    if bAlphaTex is not None:
                        bAlphaTex.image.save(f'{bDir}/{bAlphaTex.name}.png')
                    bMainTex.image.save(f'{bDir}/{bMainTex.name}.png')
                else: # Char has only front spine
                    fSkelA = readFromPathId(charATree['_skeleton'], monobehaviours)
                    fSkelDA = readFromPathId(fSkelA.read_typetree()['skeletonDataAsset'], monobehaviours)
                    fSkelFile = readFromPathId(fSkelDA.read_typetree()['skeletonJSON'], textassets)
                    fAtlasA = readFromPathId(fSkelDA.read_typetree()['atlasAssets'][0], monobehaviours)
                    fAtlasFile = readFromPathId(fAtlasA.read_typetree()['atlasFile'], textassets)
                    fMats = readFromPathId(fAtlasA.read_typetree()['materials'][0], materials)
                    for tex in fMats.read_typetree()['m_SavedProperties']['m_TexEnvs']:
                        if tex[0] == '_AlphaTex':
                            fAlphaTex = readFromPathId(tex[1]['m_Texture'], texture2ds)
                        elif tex[0] == '_MainTex':
                            fMainTex = readFromPathId(tex[1]['m_Texture'], texture2ds)

                    charName = fMainTex.name
                    fDir = f'{batDir}/{charName}/front'
                    if not os.path.exists(expDir):
                        os.mkdir(expDir)
                    if not os.path.exists(batDir):
                        os.mkdir(batDir)
                    if not os.path.exists(f'{batDir}/{charName}'):
                        os.mkdir(f'{batDir}/{charName}')
                    if not os.path.exists(fDir):
                        os.mkdir(fDir)

                    open(f'{fDir}/{fSkelFile.name}', 'wb').write(fSkelFile.script)
                    open(f'{fDir}/{fAtlasFile.name}', 'wb').write(fAtlasFile.script)
                    if fAlphaTex is not None:
                        fAlphaTex.image.save(f'{fDir}/{fAlphaTex.name}.png')
                    fMainTex.image.save(f'{fDir}/{fMainTex.name}.png')

            elif not (any(value not in charATree.keys() for value in ['_centerTransform', '_shadowTransform'])): # Build spine
                fSkelA = readFromPathId(charATree['_skeleton'], monobehaviours)
                fSkelDA = readFromPathId(fSkelA.read_typetree()['skeletonDataAsset'], monobehaviours)
                fSkelFile = readFromPathId(fSkelDA.read_typetree()['skeletonJSON'], textassets)
                fAtlasA = readFromPathId(fSkelDA.read_typetree()['atlasAssets'][0], monobehaviours)
                fAtlasFile = readFromPathId(fAtlasA.read_typetree()['atlasFile'], textassets)
                fMats = readFromPathId(fAtlasA.read_typetree()['materials'][0], materials)
                for tex in fMats.read_typetree()['m_SavedProperties']['m_TexEnvs']:
                    if tex[0] == '_AlphaTex':
                        fAlphaTex = readFromPathId(tex[1]['m_Texture'], texture2ds)
                    elif tex[0] == '_MainTex':
                        fMainTex = readFromPathId(tex[1]['m_Texture'], texture2ds)

                charName = fMainTex.name
                fDir = f'{buiDir}/{charName}'
                if not os.path.exists(expDir):
                    os.mkdir(expDir)
                if not os.path.exists(buiDir):
                    os.mkdir(buiDir)
                if not os.path.exists(fDir):
                    os.mkdir(fDir)

                open(f'{fDir}/{fSkelFile.name}', 'wb').write(fSkelFile.script)
                open(f'{fDir}/{fAtlasFile.name}', 'wb').write(fAtlasFile.script)
                if fAlphaTex is not None:
                    fAlphaTex.image.save(f'{fDir}/{fAlphaTex.name}.png')
                fMainTex.image.save(f'{fDir}/{fMainTex.name}.png')
                
        if count == 0:
            print(f'Nothing was found for: {file}')
    # except:
    #     print(f'Error: {file}')
    #     continue


# Spine assets hierarchy tree (normal)
# 
#                                               CharacterAnimator
#                                                |              |
#                                                |              |
#                           SkeletonAnimation (front)         SkeletonAnimation (back)
#                                       |                               |
#                                       |                               |
#                           SkeletonDataAsset (front)         SkeletonDataAsset (back)
#                           |               |                       |               |
#                           |               |                       |               |
#                   AtlasAssets       SkeletonFile              AtlasAssets       SkeletonFile
#                   |       |                                   |       |
#                   |       |                                   |       |
#               AtlasFile   Materials                       AtlasFile   Materials
#                           |       |                                   |       |
#                           |       |                                   |       |
#                       AlphaTex  MainTex                           AlphaTex    MainTex


# Spine assets hierarchy tree (skadi2, sora, aglina, heidi, ulika)
# 
#                                               SingleSpineAnimator
#                                                       |
#                                                       |
#                                               SkeletonAnimation
#                                                       |
#                                                       |
#                                               SkeletonDataAsset
#                                                 |           |
#                                                 |           |
#                                         AtlasAssets       SkeletonFile
#                                         |       |
#                                         |       |
#                                     AtlasFile   Materials
#                                                 |       |
#                                                 |       |
#                                             AlphaTex  MainTex


# Spine assets hierarchy tree (base)
#                                                   VCharacter
#                                                       |
#                                                       |
#                                               SkeletonAnimation
#                                                       |
#                                                       |
#                                               SkeletonDataAsset
#                                                 |           |
#                                                 |           |
#                                         AtlasAssets       SkeletonFile
#                                         |       |
#                                         |       |
#                                     AtlasFile   Materials
#                                                 |       |
#                                                 |       |
#                                             AlphaTex  MainTex