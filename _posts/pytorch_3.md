파이토치 프로젝트 템플릿



## Pytorch Project Template Overview

* 다양한 프로젝트 템플릿 존재
* 사용자 필요에 따라 수정하여 사용
* 실행, 데이터, 모델, 설정, 로깅, 지표, 유틸 등 다양한 모듈들을 분리하여 프로젝트 템플릿화



### Pytorch Template 추천 repository

* https://github.com/FrancescoSaverioZuppichini/PyTorch-Deep-Learning-Template

* https://github.com/PyTorchLightning/deep-learning-project-template

* https://github.com/victoresque/pytorch-template



## Module 구성



![pytorchtemplate](https://user-images.githubusercontent.com/120040458/224985069-77ad9afa-0f1e-4d13-be07-bedb1663172a.PNG)

<p align="center">출처 : https://github.com/victoresque/pytorch-template</p>



### train.py

```python
if __name__ == '__main__':
    args = argparse.ArgumentParser(description='PyTorch Template')
    args.add_argument('-c', '--config', default=None, type=str,
                      help='config file path (default: None)')
    args.add_argument('-r', '--resume', default=None, type=str,
                      help='path to latest checkpoint (default: None)')
    args.add_argument('-d', '--device', default=None, type=str,
                      help='indices of GPUs to enable (default: all)')

    # custom cli options to modify configuration from default values given in json file.
    CustomArgs = collections.namedtuple('CustomArgs', 'flags type target')
    options = [
        CustomArgs(['--lr', '--learning_rate'], type=float, target='optimizer;args;lr'),
        CustomArgs(['--bs', '--batch_size'], type=int, target='data_loader;args;batch_size')
    ]
    config = ConfigParser.from_args(args, options)
    main(config)
```



### parse_config.py

```python
class ConfigParser:
    def __init__(self, config, resume=None, modification=None, run_id=None):
        """
        class to parse configuration json file. Handles hyperparameters for training, initializations of modules, checkpoint saving
        and logging module.
        :param config: Dict containing configurations, hyperparameters for training. contents of `config.json` file for example.
        :param resume: String, path to the checkpoint being loaded.
        :param modification: Dict keychain:value, specifying position values to be replaced from config dict.
        :param run_id: Unique Identifier for training processes. Used to save checkpoints and training log. Timestamp is being used as default
        """
        # load config file and apply modification
        self._config = _update_config(config, modification)
        self.resume = resume

        # set save_dir where trained model and log will be saved.
        save_dir = Path(self.config['trainer']['save_dir'])

        exper_name = self.config['name']
        if run_id is None: # use timestamp as default run-id
            run_id = datetime.now().strftime(r'%m%d_%H%M%S')
        self._save_dir = save_dir / 'models' / exper_name / run_id
        self._log_dir = save_dir / 'log' / exper_name / run_id

        # make directory for saving checkpoints and log.
        exist_ok = run_id == ''
        self.save_dir.mkdir(parents=True, exist_ok=exist_ok)
        self.log_dir.mkdir(parents=True, exist_ok=exist_ok)

        # save updated config file to the checkpoint dir
        write_json(self.config, self.save_dir / 'config.json')

        # configure logging module
        setup_logging(self.log_dir)
        self.log_levels = {
            0: logging.WARNING,
            1: logging.INFO,
            2: logging.DEBUG
        }

    @classmethod
    def from_args(cls, args, options=''):
        """
        Initialize this class from some cli arguments. Used in train, test.
        """
        for opt in options:
            args.add_argument(*opt.flags, default=None, type=opt.type)
        if not isinstance(args, tuple):
            args = args.parse_args()

        if args.device is not None:
            os.environ["CUDA_VISIBLE_DEVICES"] = args.device
        if args.resume is not None:
            resume = Path(args.resume)
            cfg_fname = resume.parent / 'config.json'
        else:
            msg_no_cfg = "Configuration file need to be specified. Add '-c config.json', for example."
            assert args.config is not None, msg_no_cfg
            resume = None
            cfg_fname = Path(args.config)
        
        config = read_json(cfg_fname)
        if args.config and resume:
            # update new config for fine-tuning
            config.update(read_json(args.config))

        # parse custom cli options into dictionary
        modification = {opt.target : getattr(args, _get_opt_name(opt.flags)) for opt in options}
        return cls(config, resume, modification)
    
    ...
```



* config.json에서 불러와서 tuple형태로 만들고 ConfigParser(parse_config.py)로 넘김

  +팩토리 패턴 찾아볼것

* ConfigParser에서 read_json을 사용해서 json파일을 ordered-dict형태로 만들어주고 리턴

* config.json 에서 hyper-parameter, dataloader 등의 내용 설정



### train.py - trainer

```python
trainer = Trainer(model, criterion, metrics, optimizer,
                      config=config,
                      device=device,
                      data_loader=data_loader,
                      valid_data_loader=valid_data_loader,
                      lr_scheduler=lr_scheduler)

    trainer.train()
```

* model, dataloader, loss 등을 정해서 학습
* 실제 학습은 base_trainer를 통해



## 복습할 내용

* 프로젝트 구조
* 학습시 parse_config.py, config.json, train.py 등의 역할

